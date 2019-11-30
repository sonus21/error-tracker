Flask App Usage
---------------

Lazy initialization
~~~~~~~~~~~~~~~~~~~
    Use error_tracker.init_app method to configure

.. code::

    error_tracker = AppErrorTracker()
    ...
    error_tracker.init_app(app=app, db=db, notifier=notifier)


Config details
~~~~~~~~~~~~~~
- Enable or disable notification sending feature
   .. code::

     APP_ERROR_SEND_NOTIFICATION = False

- Email recipient list
   .. code::

      APP_ERROR_RECIPIENT_EMAIL = None

- Email subject prefix to be used by email sender
   .. code::

      APP_ERROR_SUBJECT_PREFIX = ""

- Mask value with following string
    .. code::

      APP_ERROR_MASK_WITH = "**************"

- Masking rule
    App can mask all the variables whose lower case name contains one of the configured string
    .. code::

        APP_ERROR_MASKED_KEY_HAS = ("password", "secret")

    Above configuration will mask the variable names like
     .. code::

        password
        secret
        PassWord
        THis_Is_SEcret

    .. note::
        Any variable names whose lower case string contains either *password* or *secret*


- Browse link in your service app
    List of exceptions can be seen at */dev/error*, but you can have other prefix as well due to some securities or other reasons.

    .. code::

        APP_ERROR_URL_PREFIX = "/dev/error"

- Email address used to construct Message object
    .. code::

        APP_ERROR_EMAIL_SENDER = "prod-issue@example.com"


Manual Exception Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~
Error can be tracked programmatically using AppErrorTracker's record_exception method.

.. code::

    error_tracker = AppErrorTracker(...)
    ...
    try
        ...
    catch Exception as e:
        error_tracker.record_exception()



Decorator based exception recording, record exception as it occurs in a method call.

.. note::
    Exception will be re-raised so it must be caught in the caller or ignored.


.. code::
    error_tracker = AppErrorTracker(...)
    @error_tracker.auto_track_exception
    def fun():
        pass
