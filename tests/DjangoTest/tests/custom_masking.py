import re
from django.test import TestCase
from util import TestBase
from error_tracker.django.settings import APP_ERROR_MASK_WITH


class CustomMaskingRule(TestCase, TestBase):

    def test_verify(self):
        form_data = dict(
            username="username",
            password="password")
        self.post('/post-view', data=form_data)
        errors = self.get_exceptions()
        error = errors[0]
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
            self.assertEqual(str(value), "%r" % APP_ERROR_MASK_WITH)

        for match in matches3:
            key, value = match.split(",")[0].split(" : ")
            self.assertEqual(value, "%r" % APP_ERROR_MASK_WITH)
