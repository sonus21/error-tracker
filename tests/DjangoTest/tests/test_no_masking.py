# -*- coding: utf-8 -*-
#
#    Test no masking feature
#
#    :copyright: 2023 Sonu Kumar
#    :license: BSD-3-Clause
#

import re

from django.test import TestCase
from util import TestBase
from error_tracker.django.settings import APP_ERROR_MASK_WITH


class NoMasking(TestBase, TestCase):
    def test_no_mask(self):
        self.post('/post-view', data=dict(username="username", password="password"))
        errors = self.get_exceptions()
        error = errors[0]
        re1 = r".*password.* = .*"
        re2 = r".*secret.* = .*"
        re3 = r".*form.* = .*"
        re4 = r'.*l.* = \[.*\]'
        re1 = re.compile(re1, re.IGNORECASE)
        re2 = re.compile(re2, re.IGNORECASE)
        re3 = re.compile(re3, re.IGNORECASE)
        re4 = re.compile(re4, re.IGNORECASE)

        exception = error.traceback
        matches1 = re1.findall(exception)
        matches2 = re2.findall(exception)
        self.assertEqual(len(matches1), 3)
        self.assertEqual(len(matches2), 3)
        for match in matches2 + matches1:
            key, value = match.split(" = ")
            self.assertNotEqual(value, "%r" % APP_ERROR_MASK_WITH)

        matches3 = re3.findall(exception)
        matches4 = re4.findall(exception)
        self.assertEqual(1, len(matches4))
        self.assertEqual(1, len(matches3))
        self.assertEqual("[1, 2, 3, 4]", matches4[0].strip().split("l = ")[1])
        data = matches3[0].strip().split("form = ")[1].split("QueryDict(")[1].split(')')[0]
        self.assertEqual(True, data == "{'password' : 'password', 'username' : 'username'}")
        re3 = r".*password.* : .*"
        re3 = re.compile(re3, re.IGNORECASE)
        matches3 = re3.findall(exception)
        self.assertEqual(len(matches3), 1)
        for match in matches3:
            words = match.split("' : ")
            key, value = words[0], words[1].split(",")[0]
            self.assertNotEqual(value, "%r" % APP_ERROR_MASK_WITH)
