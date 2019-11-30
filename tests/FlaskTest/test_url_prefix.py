# -*- coding: utf-8 -*-
#
#    URL prefix test, this tests whether all urls are exposed at given path prefix or not
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

import unittest
from .configs import custom_mask_rule
from .utils import TestCaseMixin


class UrlPrefixTest(TestCaseMixin):
    db_prefix = "UrlPrefixTest"
    config_module = custom_mask_rule
    kwargs = dict(url_prefix="/dev/exception/")

    def test_url(self):
        db_name = "test_url"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            c.post('/post-view')
            response = c.get(self.kwargs['url_prefix'])
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(len(response.data), 0)


if __name__ == '__main__':
    unittest.main()
