# -*- coding: utf-8 -*-
#
#    Masking rule tests
#
#    :copyright: 2018 Sonu Kumar
#    :license: BSD-3-Clause
#

import re
import unittest

from error_tracker.flask.defaults import APP_ERROR_MASK_WITH
from tests.utils import Masking
from .utils import TestCaseMixin
from .configs import masking_disabled, custom_mask_rule


class DefaultMaskingRuleTest(TestCaseMixin):
    db_prefix = "DefaultMaskingRule"

    def test_mask_key(self):
        db_name = "test_mask_key"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            c.post('/post-view')
            errors = error_tracker.get_exceptions()
            error = errors[0]
            re1 = r".*password.* = .*"
            re2 = r".*secret.* = .*"
            re1 = re.compile(re1, re.IGNORECASE)
            re2 = re.compile(re2, re.IGNORECASE)
            exception = error.traceback
            matches1 = re1.findall(exception)
            matches2 = re2.findall(exception)
            self.assertEqual(len(matches1), 3)
            self.assertEqual(len(matches2), 3)
            for match in matches2 + matches1:
                key, value = match.split(" = ")
                self.assertEqual(value, "%r" % APP_ERROR_MASK_WITH)

    def test_mask_key_form(self):
        db_name = "test_mask_key_form"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            form_data = dict(
                username="username",
                password="password")
            c.post('/post-view', data=form_data)
            errors = error_tracker.get_exceptions()
            error = errors[0]
            re1 = r".*password.* = .*"
            re2 = r".*secret.* = .*"
            re1 = re.compile(re1, re.IGNORECASE)
            re2 = re.compile(re2, re.IGNORECASE)
            exception = error.traceback
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


class NoMaskingTest(TestCaseMixin):
    db_prefix = "NoMasking"
    config_module = masking_disabled

    def test_no_mask(self):
        db_name = "test_no_mask"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            form_data = dict(
                username="username",
                password="password")
            c.post('/post-view', data=form_data)
            errors = error_tracker.get_exceptions()
            error = errors[0]
            re1 = r".*password.* = .*"
            re2 = r".*secret.* = .*"
            re1 = re.compile(re1, re.IGNORECASE)
            re2 = re.compile(re2, re.IGNORECASE)
            exception = error.traceback
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


class CustomMaskingTest(object):
    def verify(self):
        db_name = "test_mask"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            form_data = dict(
                username="username",
                password="password")
            c.post('/post-view', data=form_data)
            errors = error_tracker.get_exceptions()
            error = errors[0]
            print(error.traceback)
            re1 = r".*password.* = .*"
            re2 = r".*secret.* = .*"
            re3 = r".*password.* : .*"
            re4 = r".*key.* = .*"
            re1 = re.compile(re1, re.IGNORECASE)
            re2 = re.compile(re2, re.IGNORECASE)
            re3 = re.compile(re3, re.IGNORECASE)
            re4 = re.compile(re4, re.IGNORECASE)
            exception = error.traceback
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


class CustomMaskingRuleTest(TestCaseMixin, CustomMaskingTest):
    db_prefix = "CustomMaskingRule"
    config_module = custom_mask_rule

    def test_mask(self):
        self.verify()


class CustomMaskingClassTest(TestCaseMixin, CustomMaskingTest):
    db_prefix = "CustomMaskingClass"
    config_module = masking_disabled
    kwargs = dict(masking=Masking(custom_mask_rule.APP_ERROR_MASK_WITH,
                                  custom_mask_rule.APP_ERROR_MASKED_KEY_HAS))

    def test_mask(self):
        self.verify()


if __name__ == '__main__':
    unittest.main()
