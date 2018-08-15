import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_error import AppErrorManager
from configs import custom_mask_rule
from utils import TestCaseMixin


class UrlPrefixTest(TestCaseMixin, unittest.TestCase):
    db_prefix = "UrlPrefixTest"

    def _setup(self, db_name):
        app = Flask(__name__)
        app.config.from_object(custom_mask_rule)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_name
        db = SQLAlchemy(app)
        app.config['APP_ERROR_URL_PREFIX'] = "/dev/exception/"
        error_manager = AppErrorManager(app=app, db=db)
        db.create_all()
        return app, db, error_manager

    def test_url(self):
        db_name = "test_url"
        app, db, error_manager = self.setUpApp(db_name)
        with app.test_client() as c:
            c.post('/post-view')
            response = c.get(app.config['APP_ERROR_URL_PREFIX'])
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(len(response.data), 0)
        self.tearDownApp(db)


if __name__ == '__main__':
    unittest.main()
