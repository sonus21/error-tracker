import datetime
import unittest
from collections import namedtuple

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_error import AppErrorManager
from flask_error import ModelMixin
from test_basic import StaticTestCase


class CustomDbTest(StaticTestCase, unittest.TestCase):
    db_prefix = "CustomModelDbTest"

    def _setup(self, db_name):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_name
        db = SQLAlchemy(app)
        error_manager = AppErrorManager(app=app, db=db, db_table_name="error_db")
        db.create_all()
        return app, db, error_manager


class CustomModelClassTest(StaticTestCase, unittest.TestCase):
    db_prefix = "CustomModelClassTest"

    def _setup(self, db_name):
        app = Flask(__name__)
        Error = namedtuple("Error", "hash, host, path, method, request_data, exception, count, "
                                    "created_on, last_seen")

        class ErrorModel(ModelMixin):
            objects = {}

            @classmethod
            def delete(cls, rhash):
                cls.objects.pop(rhash)

            @classmethod
            def create_or_update(cls, rhash, host, path, method, request_data, exception):
                count = 1
                now = datetime.datetime.now()
                created_on = now
                exception = exception

                if rhash in cls.objects:
                    error = cls.objects[rhash]
                    created_on = error.created_on
                    exception = error.exception
                    count = error.count + 1
                error = Error(rhash, host, path, method, str(request_data),
                              exception, count, created_on, now)
                cls.objects[rhash] = error

            @classmethod
            def get_all(cls):
                return cls.objects.values()

            @classmethod
            def get(cls, rhash):
                error = cls.objects.get(rhash, None)
                return error

        error_manager = AppErrorManager(app=app, model=ErrorModel)
        return app, None, error_manager


if __name__ == '__main__':
    unittest.main()
