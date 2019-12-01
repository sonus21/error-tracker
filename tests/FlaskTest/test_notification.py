# -*- coding: utf-8 -*-
#
#    Notification feature tests
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

import unittest
from tests.utils import TestNotification
from .utils import TestCaseMixin
from .configs import notification_config_disabled
from .configs import notification_config_enabled


class NotificationDisabledTest(TestCaseMixin):
    db_prefix = "NotificationDisabled"
    config_module = notification_config_disabled
    notifier = TestNotification()
    kwargs = dict(notifier=notifier)

    def test_notification_disabled_flag(self):
        app, db, error_tracker = self.setUpApp("notification_disabled_flag")
        self.assertEqual(False, error_tracker.send_notification)

    def test_notification_disabled(self):
        app, db, error_tracker = self.setUpApp("notification_disabled")
        with app.test_client() as c:
            result = c.get('/value-error')
            self.assertEqual(u'500', result.data.decode('utf-8'))
            self.assertEqual(len(self.notifier.get_notifications()), 0)


class NotificationConfigurationTests(object):
    mailer = None

    def email_send(self):
        db_name = "test_notification_send"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            result = c.get('/value-error')
            self.assertEqual(u'500', result.data.decode('utf-8'))
            self.assertEqual(len(self.mailer.get_notifications()), 1)
            notification = self.mailer.get_notifications()[0]
            self.assertTrue(
                notification[0].startswith("[" + notification_config_enabled.APP_ERROR_SUBJECT_PREFIX + "]"))
            c.get('/value-error')
            self.assertEqual(len(self.mailer.get_notifications()), 2)

            c.post('/value-error')

            self.assertEqual(len(self.mailer.get_notifications()), 3)
            self.mailer.clear()

    def notification_flag_enabled(self):
        db_name = "test_notification_enabled"
        app, db, error_tracker = self.setUpApp(db_name)
        self.assertEqual(True, error_tracker.send_notification)


class NotificationEnabledTest(TestCaseMixin, NotificationConfigurationTests):
    db_prefix = "NotificationEnabled"
    mailer = TestNotification()
    kwargs = dict(notifier=mailer)
    config_module = notification_config_enabled

    def test_notification_flag_enabled(self):
        self.notification_flag_enabled()

    def test_email_send(self):
        self.email_send()


class NotificationEnabledByAppInstanceTest(TestCaseMixin, NotificationConfigurationTests):
    db_prefix = "NotificationEnabledByAppInstance"
    mailer = TestNotification()
    kwargs = dict(notifier=mailer)
    config_module = notification_config_enabled

    def test_notification_flag_enabled(self):
        self.notification_flag_enabled()

    def test_email_send(self):
        self.email_send()


if __name__ == '__main__':
    unittest.main()
