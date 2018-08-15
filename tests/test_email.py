import unittest

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from flask_error import AppErrorManager
from flask_error import MailMixin
from utils import BaseTestMixin
from configs import email_config1, email_config2


class EmailDisabled(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object(email_config1)
        app.config['SQLALCHEMY_DATABASE_URI'] = "test"
        db = SQLAlchemy(app)
        self.mailer = Mail(app=app)
        self.error_manager = AppErrorManager(app=app, db=db, mailer=self.mailer)

    def test_email_disabled(self):
        self.assertEqual(False, self.error_manager.send_email)


class EmailEnabled(BaseTestMixin, unittest.TestCase):
    db_prefix = "EmailEnabled"

    def _setup(self, db_name):
        class TestMail(MailMixin):
            emails = []

            def send(self, message):
                self.emails.append(message)

        app = Flask(__name__)
        app.config.from_object(email_config2)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_name
        db = SQLAlchemy(app)
        self.mailer = TestMail()
        error_manager = AppErrorManager(app=app, db=db,
                                        mailer=self.mailer)
        db.create_all()
        return app, db, error_manager

    def test_email_disabled(self):
        db_name = "test_email_disabled"
        app, db, error_manager = self.setUpApp(db_name)
        self.assertEqual(True, error_manager.send_email)
        self.tearDownApp(db)

    def test_email_send(self):
        db_name = "test_email_send"
        app, db, error_manager = self.setUpApp(db_name)
        with app.test_client() as c:
            result = c.get('/value-error')
            self.assertEqual(u'500', result.data.decode('utf-8'))
            self.assertEqual(len(self.mailer.emails), 1)
            c.get('/value-error')
            self.assertEqual(len(self.mailer.emails), 2)

            c.post('/value-error')

            self.assertEqual(len(self.mailer.emails), 3)
        self.tearDownApp(db)


if __name__ == '__main__':
    unittest.main()
