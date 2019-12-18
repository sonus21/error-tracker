# -*- coding: utf-8 -*-
#
#    Error tracker's flask plugin, this class initialize it's internal state
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#


from warnings import warn

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from flask import request

from error_tracker.libs.utils import Masking, ConfigError, get_exception_name, \
    get_context_detail, get_notification_subject
from error_tracker.libs.mixins import ModelMixin
from error_tracker.flask.utils import DefaultFlaskContextBuilder, DefaultFlaskViewPermission
from .view import Views
from . import defaults
import datetime

from sqlalchemy import Column, String, Text, Integer, DateTime, desc
from sqlalchemy.orm.exc import NoResultFound

page_size = None


class AppErrorTracker(object):
    def __init__(self, app=None, db=None, model=None, notifier=None, recipients=None,
                 db_table_name="app_error", notification_subject_prefix=None,
                 url_prefix=None, masking=None, ticketing=None,
                 context_builder=DefaultFlaskContextBuilder(),
                 view_permission=DefaultFlaskViewPermission()):
        """
        An error tracker class, which manage the exception and store them to database
        :param app: a Flask app instance where exception has to be tracked
        :param db: Database connection object for storing exception
        :param model: Database model object for tracking exception
        :param notifier: a notifier object that would notify notification to the subscribers
        :param recipients: list of recipients emails
        :param db_table_name: database table name in case if it's required overriding
        :param notification_subject_prefix: notification subject prefix
        :param url_prefix: URL prefix to be exposed by the web apps
        :param masking: a masking object or lambda function that can provide custom masking rules
        :param context_builder: a builder function that provides the request details,
        it can be used to provide custom data, apart from the default one
        :param ticketing:  a ticking mixing object used to create or update ticket in ticketing system
        """
        # Database related fields
        self.app = app
        self.db = db
        self.db_table = db_table_name
        self.model = model
        # masking related fields
        self.masking = masking
        # context builder object
        self.context_builder = context_builder
        self.views = None

        # notification related fields
        self.notifier = notifier
        self.notification_subject_prefix = notification_subject_prefix
        self.send_notification = False
        self.recipients = recipients
        self.notification_sender = None
        self.ticketing = ticketing
        self.view_permission = view_permission

        self.active = False
        if self.app:
            self.init_app(app, db, model=model, notifier=notifier, url_prefix=url_prefix,
                          masking=masking, context_builder=context_builder,
                          ticketing=ticketing, view_permission=view_permission)

    def init_app(self, app, db, model=None, notifier=None, url_prefix=None, masking=None,
                 context_builder=DefaultFlaskContextBuilder(),
                 ticketing=None, view_permission=DefaultFlaskViewPermission()):
        """
        Initialize this app with different attributes
        :param view_permission: view permission checker
        :param app: a Flask app instance
        :param db: Database connection object
        :param model: Database model class
        :param notifier: notifier app which will be used to notify notification
        :param url_prefix: Url prefix for WEB UI
        :param masking: a masking interface object or lambda function
        :param context_builder: a builder function that provides the request details,
        it can be used to provide custom data, apart from the default one
        :param ticketing :   a ticking mixing object used to create or update ticket in ticketing system
        :return: None
        """
        if self.active:
            raise ConfigError("App is already configured")
        self.view_permission = view_permission
        self.app = app
        self.db = db
        if app is None:
            raise ConfigError("app is None")
        if model is None and self.db is None:
            raise ConfigError("Either db or model must be provide")

        send_notification = self.app.config.setdefault('APP_ERROR_SEND_NOTIFICATION',
                                                       defaults.APP_ERROR_SEND_NOTIFICATION)
        recipients = self.app.config.setdefault('APP_ERROR_RECIPIENT_EMAIL',
                                                defaults.APP_ERROR_RECIPIENT_EMAIL)
        subject_prefix = self.app.config.setdefault('APP_ERROR_SUBJECT_PREFIX',
                                                    defaults.APP_ERROR_SUBJECT_PREFIX)
        mask_with = self.app.config.setdefault('APP_ERROR_MASK_WITH', defaults.APP_ERROR_MASK_WITH)
        mask_key_has = self.app.config.setdefault('APP_ERROR_MASKED_KEY_HAS',
                                                  defaults.APP_ERROR_MASKED_KEY_HAS)
        url_prefix = url_prefix or self.app.config.setdefault('APP_ERROR_URL_PREFIX',
                                                              defaults.APP_ERROR_URL_PREFIX)
        self.notification_sender = self.app.config.setdefault('APP_ERROR_EMAIL_SENDER',
                                                              defaults.APP_ERROR_EMAIL_SENDER)

        global page_size
        self.model = model or self._get_model()
        self.views = Views(self.app, self.model, url_prefix, self.view_permission)
        page_size = self.app.config.setdefault("APP_DEFAULT_LIST_SIZE", defaults.APP_DEFAULT_LIST_SIZE)
        # masking object setting
        if type(mask_key_has) == str:
            mask_key_has = (mask_key_has,)
        if mask_key_has and mask_with:
            self.masking = masking or Masking(mask_with, mask_key_has)

        self.notifier = notifier or getattr(app, "notifier", None) or getattr(app, "mailer", None)
        self._set_notification_fields(recipients, send_notification, subject_prefix)
        # Use the new style teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)
        self.context_builder = context_builder
        self.ticketing = ticketing
        self.active = True

    def _set_notification_fields(self, recipients, send_notification, subject_prefix):
        if self.notifier is not None and send_notification:
            if recipients not in [None, ""]:
                self.send_notification = True
                self.recipients = recipients
                if type(self.recipients) == str:
                    self.recipients = [self.recipients]
                if self.notification_sender is None:
                    raise ConfigError(
                        "Email recipients is set but notification sender is"
                        " not configured. set APP_ERROR_EMAIL_SENDER in app config")
                self.recipients = list(self.recipients)
            else:
                warn("APP_ERROR_RECIPIENT_EMAIL is not set in the app config")

            if subject_prefix in [None, ""]:
                warn("APP_ERROR_SUBJECT_PREFIX is not set in the app config")
            else:
                self.notification_subject_prefix = subject_prefix

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
            exception_name = Column(String(256))
            traceback = Column(Text)
            count = Column(Integer, default=1)
            created_on = Column(DateTime)
            last_seen = Column(DateTime)

            def __repr__(self):
                return "AppDbModel(%s)" % self.__str__()

            @classmethod
            def delete_entity(cls, rhash):
                """
                :param rhash: lookup key
                :return: None
                """
                cls.query.filter_by(hash=rhash).delete()
                cls.db.session.commit()

            @classmethod
            def create_or_update_entity(cls, rhash, host, path, method, request_data,
                                        exception_name, traceback):
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
                                exception_name=exception_name, traceback=traceback,
                                created_on=now,
                                last_seen=now)
                    cls.db.session.add(error)
                    cls.db.session.commit()
                return error

            @classmethod
            def get_exceptions_per_page(cls, page_number=1):
                return cls.query.order_by(desc(cls.last_seen)).paginate(
                    page_number, page_size, False)

            @classmethod
            def get_entity(cls, rhash):
                """
                :param rhash: key for lookup
                :return: Single entry of this class
                """
                error = cls.query.filter_by(hash=rhash).first()
                return error

            class Meta:
                table_name = self.db_table

        return AppDbModel

    def _send_notification(self, url, method, message, exception, error):
        subject = get_notification_subject(self.notification_subject_prefix,
                                           method, url, exception)
        self.notifier.notify(request, error, email_subject=subject,
                             email_body=message, from_email=self.notification_sender,
                             recipient_list=self.recipients)

    def _post_process(self, rq, frame_str, frames, error):
        if self.send_notification:
            if rq:
                message = ('URL: %s' % rq.path) + '\n\n'
                method = rq.method
                url = rq.url
            else:
                message = ""
                method = ""
                url = ""
            message += frame_str
            self._send_notification(url, method, message,
                                    frames[-1][:-1], error)
        if self.ticketing is not None:
            self.ticketing.raise_ticket(error)

    def capture_message(self, message):
        """
        Capture an error for the current error
        :param message:  message to be recorded
        :return:  None
        """
        self.capture_exception(additional_context={'message': message})

    def capture_exception(self, additional_context=None):
        """
        Record occurred exception, check whether the exception recording is
        enabled or not. If it's enabled then record all the details and store
        them in the database, it will notify email as well. The id of exception
        is SHA256 of frame string
        :return: None
        """
        rq = request
        if not self.active:
            return
        try:
            path = request.path
            host = request.host_url
            method = request.method
        except RuntimeError:
            rq = None
            path = ""
            host = ""
            method = ""

        ty, frames, frame_str, traceback_str, rhash, request_data = \
            get_context_detail(rq, self.masking, self.context_builder, additional_context)
        error = self.model.create_or_update_entity(rhash, host, path, method,
                                                   str(request_data),
                                                   get_exception_name(ty),
                                                   traceback_str)
        self._post_process(rq, frame_str, frames, error)

    def auto_track_exception(self, func, additional_context=None, silent=False):
        """
        Decorator to be used for automatic exception capture, where exception can occur
        :param func:
        :param additional_context:  any additional context
        :param silent: exception should be re-raise or ignored
        :return: None
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.capture_exception(additional_context)
                if not silent:
                    raise e

        return wrapper

    def track_exception(self, func):
        """
        Decorator to be used for automatic exception capture, on HTTP 500 etc,
        where exception has already occurred
        """

        def wrapper(e):
            self.capture_exception()
            return func(e)

        return wrapper

    def get_exceptions(self, page_number=1):
        """
        Get list of exception objects from persistence store
        :param page_number: documents of a specific page
        :return: list of exception objects
        """
        if self.model:
            return self.model.get_exceptions_per_page(page_number=page_number).items
        raise ConfigError

    def get_exception(self, rhash):
        """
        Get a specific exception, can be used for some customization etc
        :param rhash:  hash of the exception
        :return:  exception object
        """
        if self.model:
            return self.model.get_entity(rhash)
        raise ConfigError

    def delete_exception(self, rhash):
        """
        Delete a specific exception from database
        :param rhash: hash of the exception
        :return:   whatever model returns
        """
        if self.model:
            return self.model.delete_entity(rhash)
        raise ConfigError

    def create_or_update_exception(self, rhash, host, path, method, request_data,
                                   exception_name, traceback):
        if self.model:
            return self.model.create_or_update_entity(rhash, host, path, method, request_data,
                                                      exception_name, traceback)
        raise ConfigError
