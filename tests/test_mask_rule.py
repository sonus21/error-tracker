import re
import unittest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_error import AppErrorManager
from flask_error.defaults import APP_ERROR_MASK_WITH
from utils import TestCaseMixin
from configs import no_masking, custom_mask_rule


class DefaultMaskRule(TestCaseMixin, unittest.TestCase):
    db_prefix = "DefaultMaskRule"

    def test_mask_key(self):
        db_name = "test_mask_key"
        app, db, error_manager = self.setUpApp(db_name)
        with app.test_client() as c:
            c.post('/post-view')
            errors = error_manager.get_all_errors()
            error = errors[0]
            re1 = r".*password.* = .*"
            re2 = r".*secret.* = .*"
            re1 = re.compile(re1, re.IGNORECASE)
            re2 = re.compile(re2, re.IGNORECASE)
            exception = error.exception
            matches1 = re1.findall(exception)
            matches2 = re2.findall(exception)
            self.assertEqual(len(matches1), 3)
            self.assertEqual(len(matches2), 3)
            for match in matches2 + matches1:
                key, value = match.split(" = ")
                self.assertEqual(value, "%r" % APP_ERROR_MASK_WITH)
        self.tearDownApp(db)

    def test_mask_key_form(self):
        db_name = "test_mask_key_form"
        app, db, error_manager = self.setUpApp(db_name)
        with app.test_client() as c:
            form_data = dict(
                username="username",
                password="password")
            c.post('/post-view', data=form_data)
            errors = error_manager.get_all_errors()
            error = errors[0]
            re1 = r".*password.* = .*"
            re2 = r".*secret.* = .*"
            re1 = re.compile(re1, re.IGNORECASE)
            re2 = re.compile(re2, re.IGNORECASE)
            exception = error.exception
            print("EXCEPTION", exception)
            matches1 = re1.findall(exception)
            matches2 = re2.findall(exception)
            self.assertEqual(len(matches1), 3)
            self.assertEqual(len(matches2), 3)
            for match in matches2 + matches1:
                key, value = match.split(" = ")
                self.assertEqual(value, "%r" % APP_ERROR_MASK_WITH)

            re3 = r".*password.* : .*"
            re3 = re.compile(re3, re.IGNORECASE)
            matches3 = re3.findall(exception)
            self.assertEqual(len(matches3), 1)
            for match in matches3:
                words = match.split("' : ")
                key, value = words[0], words[1].split(",")[0]
                self.assertEqual(value, "%r" % APP_ERROR_MASK_WITH)
        self.tearDownApp(db)


class NoMasking(TestCaseMixin, unittest.TestCase):
    db_prefix = "NoMasking"

    def _setup(self, db_name):
        app = Flask(__name__)
        app.config.from_object(no_masking)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_name
        db = SQLAlchemy(app)
        error_manager = AppErrorManager(app=app, db=db)
        db.create_all()
        return app, db, error_manager

    def test_no_mask(self):
        db_name = "test_no_mask"
        app, db, error_manager = self.setUpApp(db_name)
        with app.test_client() as c:
            form_data = dict(
                username="username",
                password="password")
            c.post('/post-view', data=form_data)
            errors = error_manager.get_all_errors()
            error = errors[0]
            re1 = r".*password.* = .*"
            re2 = r".*secret.* = .*"
            re1 = re.compile(re1, re.IGNORECASE)
            re2 = re.compile(re2, re.IGNORECASE)
            exception = error.exception
            matches1 = re1.findall(exception)
            matches2 = re2.findall(exception)
            self.assertEqual(len(matches1), 3)
            self.assertEqual(len(matches2), 3)
            for match in matches2 + matches1:
                key, value = match.split(" = ")
                self.assertNotEqual(value, "%r" % APP_ERROR_MASK_WITH)

            re3 = r".*password.* : .*"
            re3 = re.compile(re3, re.IGNORECASE)
            matches3 = re3.findall(exception)
            self.assertEqual(len(matches3), 1)
            for match in matches3:
                words = match.split("' : ")
                key, value = words[0], words[1].split(",")[0]
                self.assertNotEqual(value, "%r" % APP_ERROR_MASK_WITH)

        self.tearDownApp(db)


class CustomMaskingRule(TestCaseMixin, unittest.TestCase):
    db_prefix = "CustomMaskingRule"

    def _setup(self, db_name):
        app = Flask(__name__)
        app.config.from_object(custom_mask_rule)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_name
        db = SQLAlchemy(app)
        error_manager = AppErrorManager(app=app, db=db)
        db.create_all()
        return app, db, error_manager

    def test_mask(self):
        db_name = "test_mask"
        app, db, error_manager = self.setUpApp(db_name)
        with app.test_client() as c:
            form_data = dict(
                username="username",
                password="password")
            c.post('/post-view', data=form_data)
            errors = error_manager.get_all_errors()
            error = errors[0]
            print(error.exception)
            re1 = r".*password.* = .*"
            re2 = r".*secret.* = .*"
            re3 = r".*password.* : .*"
            re4 = r".*key.* = .*"
            re1 = re.compile(re1, re.IGNORECASE)
            re2 = re.compile(re2, re.IGNORECASE)
            re3 = re.compile(re3, re.IGNORECASE)
            re4 = re.compile(re4, re.IGNORECASE)
            exception = error.exception
            matches1 = re1.findall(exception)
            matches2 = re2.findall(exception)
            matches3 = re3.findall(exception)
            matches4 = re4.findall(exception)

            self.assertEqual(len(matches1), 3)
            self.assertEqual(len(matches2), 3)
            self.assertEqual(len(matches3), 1)
            self.assertEqual(len(matches4), 1)

            for match in matches2 + matches1 + matches4:
                key, value = match.split(" = ")
                self.assertEqual(str(value), "%r" % custom_mask_rule.APP_ERROR_MASK_WITH)

            for match in matches3:
                key, value = match.split(",")[0].split(" : ")
                self.assertEqual(value, "%r" % custom_mask_rule.APP_ERROR_MASK_WITH)
        self.tearDownApp(db)


if __name__ == '__main__':
    unittest.main()
