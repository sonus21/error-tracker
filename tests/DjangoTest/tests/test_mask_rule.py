# -*- coding: utf-8 -*-
#
#    Masking rule tests
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

import re
import unittest

from django.test import TestCase
from util import TestBase
from error_tracker.django.settings import APP_ERROR_MASK_WITH


class DefaultMaskingRule(TestBase, TestCase):
    def test_mask_key(self):
        self.post('/post-view')
        errors = self.get_exceptions()
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
        form_data = dict(
            username="username",
            password="password")
        self.post('/post-view', data=form_data)
        errors = self.get_exceptions()
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
            self.assertEqual(value, u"%r" % APP_ERROR_MASK_WITH)



if __name__ == '__main__':
    unittest.main()
