# -*- coding: utf-8 -*-


import sys
import traceback
from hashlib import sha256

import os
from flask import abort
from flask import blueprints
from flask import redirect
from flask import url_for
from warnings import warn

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from flask import render_template
from flask import request

from flask_mail import Message
from .exception_formatter import format_exception
from .utils import Maskable, ConfigError
from .mixins import ModelMixin
import defaults
import datetime

from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.orm.exc import NoResultFound

root_path = os.path.abspath(os.path.dirname(__file__))

blueprint = blueprints.Blueprint("app_error", 'app_error',
                                 root_path=root_path,
                                 template_folder="templates")

_Model = None


class AppErrorManager(object):
    def __init__(self, app=None, db=None, model=None, mailer=None, recipients=None,
                 db_table_name="app_error", email_subject_prefix=None,
                 url_prefix=None, maskable=None):
        self.app = app
        self.db = db
        self.db_table = db_table_name
        self.model = model
        self.recipients = recipients
        self.email_subject_prefix = email_subject_prefix
        self.send_email = False
        self.active = False
        self.maskable = maskable
        self.mailer = mailer
        self.email_sender = None
        if self.app:
            self.init_app(app, db, model=model, mailer=mailer, url_prefix=url_prefix, maskable=maskable)

    def get_request_details(self):
        """
        :return: Get request data in dict format for storing in DB
        """
        form = dict(request.form)
        if self.maskable:
            for key in form:
                masked, value = self.maskable(key)
                if masked:
                    form[key] = value
        request_data = str({
            'args': dict(request.args),
            'form': form
        })
        return request_data

    def init_app(self, app, db, model=None, mailer=None, url_prefix=None, maskable=None):
        """
        Initialize this app with different attributes
        :param app: a Flask app instance
        :param db: Database connection object
        :param model: Database model class
        :param mailer: Mail app which will be used to send email
        :param url_prefix: Url prefix for WEB UI
        :return: None
        """
        self.app = app
        self.db = db
        if app is None:
            raise ConfigError("app is None")
        if model is None and self.db is None:
            raise ConfigError("Either db or model must be provide")

        self.mailer = mailer or getattr(app, "mailer", None)
        self.model = model or self._get_model()

        send_email = self.app.config.setdefault('APP_ERROR_SEND_EMAIL',
                                                defaults.APP_ERROR_SEND_EMAIL)
        recipients = self.app.config.setdefault('APP_ERROR_RECIPIENT_EMAIL',
                                                defaults.APP_ERROR_RECIPIENT_EMAIL)
        subject_prefix = self.app.config.setdefault('APP_ERROR_SUBJECT_PREFIX',
                                                    defaults.APP_ERROR_SUBJECT_PREFIX)
        mask_with = self.app.config.setdefault('APP_ERROR_MASK_WITH', defaults.APP_ERROR_MASK_WITH)
        mask_key_has = self.app.config.setdefault('APP_ERROR_MASKED_KEY_HAS',
                                                  defaults.APP_ERROR_MASKED_KEY_HAS)
        url_prefix = url_prefix or self.app.config.setdefault('APP_ERROR_URL_PREFIX',
                                                              defaults.APP_ERROR_URL_PREFIX)
        global blueprint
        blueprint.url_prefix = url_prefix
        self.app.register_blueprint(blueprint)
        if self.mailer is not None and send_email:
            if recipients not in [None, ""]:
                self.send_email = True
                self.recipients = recipients
                if type(self.recipients) == str:
                    self.recipients = [self.recipients]
                self.recipients = list(self.recipients)
            else:
                warn("APP_ERROR_RECIPIENT_EMAIL is not set in the app config")

            if subject_prefix in [None, ""]:
                warn("APP_ERROR_SUBJECT_PREFIX is not set in the app config")

        self.active = True

        # Maskable object setting
        if type(mask_key_has) == str:
            mask_key_has = (mask_key_has,)
        if mask_key_has and mask_with:
            self.maskable = maskable or Maskable(mask_with, mask_key_has)
        self.email_sender = self.app.config.setdefault('APP_ERROR_EMAIL_SENDER',
                                                       defaults.APP_ERROR_EMAIL_SENDER)
        if self.send_email and self.email_sender is None:
            raise ConfigError("Email sender is not configured. set APP_ERROR_EMAIL_SENDER in app config")

        global _Model
        _Model = self.model

        # Use the new style teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        pass

    def _get_model(self):
        """
        :return: Default model for storing exception
        """

        class AppDbModel(ModelMixin, self.db.Model):
            db = self.db
            hash = Column(String(64), primary_key=True)
            host = Column(String(2048))
            path = Column(String(512))
            method = Column(String(32))
            request_data = Column(Text)
            exception = Column(Text)
            count = Column(Integer, default=1)
            created_on = Column(DateTime)
            last_seen = Column(DateTime)

            def __repr__(self):
                return "AppDbModel(%s)" % self.__str__()

            @classmethod
            def delete(cls, rhash):
                """
                :param rhash: lookup key
                :return: None
                """
                cls.query.filter_by(hash=rhash).delete()
                cls.db.session.commit()

            @classmethod
            def create_or_update(cls, rhash, host, path, method, request_data, exception):
                """
                :param rhash: Key of the db entry
                :param host: App host e.g. example.com
                :param path: request path
                :param method: request method (GET/POST/PUT etc)
                :param request_data: request form data
                :param exception: Exception data captured
                :return:  None
                """
                try:
                    error = cls.query.filter_by(hash=rhash).one()
                    error.count += 1
                    error.last_seen = datetime.datetime.now()
                    # error.exception = exception
                    cls.db.session.commit()
                except NoResultFound:
                    now = datetime.datetime.now()
                    error = cls(hash=rhash, host=host, path=path, method=method,
                                request_data=str(request_data),
                                exception=exception, created_on=now,
                                last_seen=now)
                    cls.db.session.add(error)
                    cls.db.session.commit()

            @classmethod
            def get_all(cls):
                """
                :return: All entries from the store
                """
                return cls.query.order_by("last_seen desc").all()

            @classmethod
            def get(cls, rhash):
                """
                :param rhash: key for lookup
                :return: Single entry of this class
                """
                error = cls.query.filter_by(hash=rhash).first()
                return error

            class Meta:
                table_name = self.db_table

        return AppDbModel

    def _send_email(self, url, method, message, exception=""):
        if self.email_subject_prefix:
            subject = "[%s][%s] %s" % (self.email_subject_prefix, method, url)
        else:
            subject = "[%s] %s" % (method, url)
        if exception:
            subject = "[%s] %s" % (exception, subject)

        msg = Message(body=message, subject=subject, recipients=self.recipients,
                      sender=self.email_sender)
        self.mailer.send(msg)

    def record_error(self):
        """
        Record occurred exception
        :return:
        """
        if not self.active:
            return
        path = request.path
        host = request.host_url
        method = request.method
        ty, val, tb = sys.exc_info()
        frames = traceback.format_exception(ty, val, tb)
        exception = format_exception(ty, val, tb, maskable=self.maskable)
        frame_str = ''.join(frames)
        rhash = sha256(frame_str).hexdigest()
        request_data = self.get_request_details()
        self.model.create_or_update(rhash, host, path, method, str(request_data), exception)

        if self.send_email:
            message = ('URL: %s' % request.path) + '\n\n'
            message += frame_str
            self._send_email(request.url, request.method, message, exception=frames[-1][:-1])

    def record_error_required(self, func):
        """
        Decorator to be used for automatic exception capture
        """

        def wrapper(e):
            self.record_error()
            return func(e)

        return wrapper

    def get_all_errors(self):
        if self.model:
            return self.model.get_all()
        raise ConfigError

    def get_error(self, rhash):
        if self.model:
            return self.model.get(rhash)
        raise ConfigError

    def delete_error(self, rhash):
        if self.model:
            return self.model.get()
        raise ConfigError


@blueprint.route('/')
def view_list():
    error = "Flask Error not configure"
    title = "App Error"
    errors = []
    if _Model:
        error = False
        errors = _Model.get_all()
    return render_template('list.html', error=error, title=title, errors=errors)


@blueprint.route('/<string:rhash>')
def view_detail(rhash):
    title = "App Error"
    error = "Flask Error not configure"
    obj = None
    if _Model:
        obj = _Model.get(rhash)
        error = False
        if obj is None:
            abort(404)
        title = "%s : %s" % (obj.method, obj.path)

    return render_template('detail.html', error=error, title=title, obj=obj)


@blueprint.route('/delete/<string:rhash>')
def view_delete(rhash):
    if _Model:
        _Model.delete(rhash)
    return redirect(url_for('app_error.view_list'))
