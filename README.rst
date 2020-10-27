=============
Error Tracker
=============

**Full featured error tracking module for Python apps supports Flask and Django**

.. image::  https://img.shields.io/pypi/v/error-tracker.svg?color=dark-green
    :target: https://pypi.org/project/error-tracker

.. image::  https://img.shields.io/pypi/pyversions/error-tracker.svg?color=dark-green
    :target: https://pypi.org/project/error-tracker

.. image:: https://img.shields.io/github/license/sonus21/error-tracker.svg?color=dark-green
    :target: https://github.com/sonus21/error-tracker/blob/master/LICENSE.txt

.. image:: https://travis-ci.org/sonus21/error-tracker.svg?branch=master
    :target: https://travis-ci.org/sonus21/error-tracker

.. image:: https://coveralls.io/repos/github/sonus21/error-tracker/badge.svg?color=dark-green
    :target: https://coveralls.io/github/sonus21/error-tracker

Introduction
------------
ErrorTracker is a batteries-included app and extensions for python app, that can track errors, send notification, mask sensitive data and capture frames data.

It plays nicely with `Django <https://www.djangoproject.com/>`_ and `Flask <http://flask.pocoo.org/>`_

Simple to use  extension that lets you add error recording interfaces to Python applications.
It's implemented in such a way that the developer has total control of the resulting application.

Out-of-the-box, Error Tracker plays nicely with various ORM's, including

- `SQLAlchemy <http://www.sqlalchemy.org/>`_,
- `MongoEngine <http://mongoengine.org/>`_,
- `Django ORM <https://tutorial.djangogirls.org/en/django_orm/>`_


It also boasts a simple Model management interface.

The biggest feature of ErrorTracker is flexibility. To start off with you can create a very simple application in no time,
with exception monitor enabled, but then you can go further and customize different aspects.

ErrorTracker is an active project, well-tested and production ready.

Installation
------------
To install ErrorTracker, simply::

    pip install error-tracker


Features
--------
- Sensitive data( like *password*, *secret* ) Masking
- Record all the frames ( frame data are stored in JSON format so that it can be analyzed later)
- Unique URL generation
- Number of times the exception occurred and first/last time of exception
- Sending notifications with exception details
- Record different types of exception like 500 or 404 etc
- Raise or update ticket in Jira/Bugzilla etc by ticketing interface.

Usage
-----

Flask App configuration
=======================

.. code::

    ...
    APP_ERROR_SEND_EMAIL = True
    APP_ERROR_RECIPIENT_EMAIL = ('example@example.com',)
    APP_ERROR_SUBJECT_PREFIX = "Server Error"
    APP_ERROR_EMAIL_SENDER = 'user@example.com'



app.py

.. code::

    from flask import Flask
    from flask_mail import Mail
    import settings
    from error_tracker import AppErrorTracker, NotificationMixin
    from flask_sqlalchemy import SQLAlchemy
    ...
    app = Flask(__name__)
    app.config.from_object(settings)
    db = SQLAlchemy(app)
    class Notifier(Mail, NotificationMixin):
        def notify(self, request, exception,
                   email_subject=None,
                   email_body=None,
                   from_email=None,
                   recipient_list=None):
            message = Message(email_subject, recipient_list, email_body, sender=from_email)
            self.send(message)
    mailer = Notifier(app=app)
    error_tracker = AppErrorTracker(app=app, db=db, notifier=mailer)

    ....

    ....
    # Record exception when 404 error code is raised
    @app.errorhandler(403)
    def error_403(e):
        error_tracker.capture_exception()
        # any custom logic

    # Record error using decorator
    @app.errorhandler(500)
    @error_tracker.track_exception
    def error_500(e):
        # some custom logic
    ....


Django App Usage
================

We need to update settings.py file as

-  Add app to installed apps list
-  Add Middleware for exception tracking. This should be added at the end so that it can process exception 1st in the middleware call stack.
-  Other configs related to notification

Sample Code


.. code::

    ...
    APP_ERROR_RECIPIENT_EMAIL = ('example@example.com',)
    APP_ERROR_SUBJECT_PREFIX = "Server Error"
    APP_ERROR_EMAIL_SENDER = 'user@example.com'

    INSTALLED_APPS = [
        ...
        'error_tracker.DjangoErrorTracker'
    ]
    MIDDLEWARE = [
        ...
        'error_tracker.django.middleware.ExceptionTrackerMiddleWare'
    ]


Documentations
--------------
This has got extensive document browse at https://error-tracker.readthedocs.io/en/latest/

All docs are in `docs/source`

And if you want to preview any *.rst* snippets that you may want to contribute, go to `http://rst.ninjs.org/ <http://rst.ninjs.org/>`_.


Examples
--------
Several usage examples are included in the */tests* folder. Please feel free to add your own examples, or improve
on some of the existing ones, and then submit them via GitHub as a *pull-request*.

You can see some of these examples in action at https://github.com/sonus21/error-tracker/tree/master/examples
To run the examples on your local environment, one at a time, do something like::

    cd error-tracker/examples


Django::

     cd error-tracker/examples
     cd DjangoSample
     python manage.py runserver

Flask::

      cd flask-sample
      python app.py


Tests
-----
To run the tests, from the project directory, simply::

    pip install -r requirements-dev.txt
    bash run-tests.sh

You should see output similar to::

    .............................................
    ----------------------------------------------------------------------
    Ran 31 tests in 1.144s

    OK


Contribution
-------------
You're most welcome to raise pull request or fixes.
