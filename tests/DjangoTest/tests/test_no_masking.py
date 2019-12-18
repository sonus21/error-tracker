# -*- coding: utf-8 -*-
#
#    Test no masking feature
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#

import re

from django.test import TestCase
from util import TestBase
from error_tracker.django.settings import APP_ERROR_MASK_WITH


class NoMasking(TestBase, TestCase):
    def test_no_mask(self):
        self.post('/post-view', data=dict(
            username="username",
            password="password"))
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
            self.assertNotEqual(value, "%r" % APP_ERROR_MASK_WITH)

        re3 = r".*password.* : .*"
        re3 = re.compile(re3, re.IGNORECASE)
        matches3 = re3.findall(exception)
        self.assertEqual(len(matches3), 1)
        for match in matches3:
            words = match.split("' : ")
            key, value = words[0], words[1].split(",")[0]
            self.assertNotEqual(value, "%r" % APP_ERROR_MASK_WITH)
