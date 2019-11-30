Notification notify feature
----------------------------
Notifications are very useful in the case of failure, in different situations notification can be used to notify users using different channels like Slack, Email etc.
Notification feature can be enabled by providing a *NotificationMixin* object.

.. code::

       from error_tracker import NotificationMixin
        class Notifier(NotificationMixin):
            def notify(self, request, exception,
                       email_subject=None,
                       email_body=None,
                       from_email=None,
                       recipient_list=None):
                # add logic here



Flask App Usage
===============

.. code::

    error_tracker = AppErrorTracker(app=app, db=db, notifier=Notifier())

Django App Usage
================
**settings.py**

.. code::

    APP_ERROR_NOTIFICATION_MODULE = "path to Notifier class"


