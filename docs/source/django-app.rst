Django App Settings
-------------------

Error Tracker fits nicely with Django framework, error tracker can be configured in different ways.
Multiple settings are available, these settings can be configured using settings file.

Setting details
~~~~~~~~~~~~~~~

- Home page list size, display 10 exceptions per page

 .. code::

  EXCEPTION_APP_DEFAULT_LIST_SIZE = 10

- What all sensitive data should be masked

  .. code::

    APP_ERROR_MASKED_KEY_HAS =  ("password", "secret")

 .. note::
    This means any variables whose name have either password or secret would be masked

- Sensitive data masking value

    .. code::

        APP_ERROR_MASK_WITH = '*************'

- Exception email subject prefix

    .. code::

        APP_ERROR_SUBJECT_PREFIX = get('APP_ERROR_SUBJECT_PREFIX', '')

- Email sender's email id
    .. code::

        APP_ERROR_EMAIL_SENDER = "server@example.com"

- Whom email should be sent in the case of failure

    .. code::

        APP_ERROR_RECIPIENT_EMAIL = ('dev-group1@example.com', 'dev@example.com')
- By default only 500 errors are tracked but HTTP 404, 401 etc can be tracked as well

    .. code::

        TRACK_ALL_EXCEPTIONS = True

.. note::
    Below configurations are required path to some class.

- Custom Masking Module

    .. code::

        APP_ERROR_MASKING_MODULE = "path to Masking class"

- Ticketing/Bugging module

    .. code::

        APP_ERROR_TICKETING_MODULE = "path to Ticketing class"

    .. note::
        Class must not have any constructor arguments

- Notifier module

    .. code::

        APP_ERROR_NOTIFICATION_MODULE = "path to Notification class"

    .. note::
        Class must not have any constructor arguments

- Context Builder module

    .. code::

        APP_ERROR_CONTEXT_BUILDER_MODULE = "path to ContextBuilder class"

    .. note::
        Class must not have any constructor arguments

- Custom Model used for exceptions storage
    .. code::

        APP_ERROR_DB_MODEL = "path to Model class"

    .. note::
        Class must implements all abstract methods


Manual Exception Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~

Error can be tracked programmatically using ErrorTracker's object available in middleware module. For tracking exception call
error_tracker.record_exception method.

.. code::

    from error_tracker.django.middleware import error_tracker

    ...
    try
        ...
    catch Exception as e:
        error_tracker.record_exception(request, e)

Decorator based exception recording, record exception as it occurs in a method call.

.. note::
    Exception will be re-raised so it must be caught in the caller or ignored.

.. code::

    from error_tracker.django.middleware import track_exception

    @track_exception
    def do_something():
        ...

