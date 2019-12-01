# -*- coding: utf-8 -*-
#
#    Notification feature tests
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

import unittest
from django.test import TestCase
from util import TestBase
from DjangoTest.notification_settings import APP_ERROR_SUBJECT_PREFIX


class NotificationConfigurationTests(TestBase, TestCase):
    def test_email_send(self):
        self.get('/value-error')
        notifications = self.get_notifications()
        self.assertEqual(len(notifications), 1)
        self.assertTrue(APP_ERROR_SUBJECT_PREFIX in notifications[0][0])
        self.get('/value-error')
        self.assertEqual(len(self.get_notifications()), 2)
        self.post('/value-error')
        self.assertEqual(len(self.get_notifications()), 3)
        self.clear_notifications()


if __name__ == '__main__':
    unittest.main()
