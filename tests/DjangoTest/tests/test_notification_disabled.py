# -*- coding: utf-8 -*-
#
#    Notification feature disabled
#
#    :copyright: 2018 Sonu Kumar
#    :license: BSD-3-Clause
#

import unittest
from django.test import TestCase
from util import TestBase
from error_tracker.django.middleware import notifier


class NotificationDisabledTest(TestBase, TestCase):
    def test_email_send(self):
        self.assertIsNone(notifier)


if __name__ == '__main__':
    unittest.main()
