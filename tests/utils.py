import logging

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

from flask_error import AppErrorManager


class BaseTestMixin(object):
    log_file = "flask_error_monitor.log"
    db_prefix = ""

    def get_db_name(self, db_name):
        if len(self.db_prefix) != 0:
            return "%s-%s.sqlite" % (self.db_prefix, db_name)
        raise ValueError

    def _setup(self, db_name):
        raise NotImplemented

    def setUpApp(self, db_name):
        db_name = self.get_db_name(db_name)
        app, db, error_manager = self._setup(db_name)
        l = logging.getLogger(__name__)
        formatter = logging.Formatter('%(message)s')
        fileHandler = logging.FileHandler(self.log_file)
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.setLevel(logging.DEBUG)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)

        self.logger = l

        @app.route('/')
        def index():
            return u'No Exception!'

        @app.route("/value-error", methods=['GET', 'POST'])
        def view_value_error():
            raise ValueError

        @app.route("/post-view", methods=['POST'])
        def post_view():
            form = request.form
            password = "qwerty"
            secret = "pass"
            key = "key"
            foo_secret = "THIS IS SECRET"
            test_password_test = "test_password_test"
            TestPassWordTest = "TestPassWordTest"
            TestSecret = "TESTSECRET"
            l = [1, 2, 3, 4]
            t = (1, 2, 3, 4)
            d = {'test': 100, "1": 1000}
            print(form, password, secret, key, d, foo_secret,
                  TestPassWordTest, test_password_test, TestSecret, l, t, d)
            print(d['KeyError'])
            return "KeyError"

        @app.errorhandler(500)
        @error_manager.record_error_required
        def error_500(e):
            return u"500", 500

        return app, db, error_manager

    def tearDownApp(self, db):
        if db:
            db.drop_all()

    def write(self, data):
        with open("log.log", "a") as f:
            f.write("*" * 100)
            f.write("\n")
            f.write(str(data))
            f.write("\n")
            f.write("*" * 100)
            f.write("\n")


class TestCaseMixin(BaseTestMixin):
    def _setup(self, db_file):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_file
        db = SQLAlchemy(app)
        error_manager = AppErrorManager(app=app, db=db)
        db.create_all()
        return app, db, error_manager
