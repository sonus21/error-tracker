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
Error can be tracked programmatically using AppErrorTracker's capture_exception method.
ErrorTracker provides many ways to capture error.

Capture Error using `capture_exception` method
`capture_exception` takes another parameter for `additional_context`  (dictionary of key value pairs).
This parameter can be used to provide additional details about the failure.


.. code::

    error_tracker = AppErrorTracker(...)
    ...
    try
        ...
    catch Exception as e:
        error_tracker.capture_exception()


A simple Message can be captured using `capture_message` method.


.. code::

    try
        ...
    catch Exception as e:
        error_tracker.capture_message("Something went wrong!")


Decorator based exception recording, record exception as it occurs in a method call.

.. note::
    Exception will be re-raised so it must be caught in the caller or ignored.
    Raised exception can be ignored by passing `silent=True`.
    Also more context detail can be provided using `additional_context` parameter.


.. code::

    @error_tracker.auto_track_exception
    def fun():
        pass


So far, you have seen only uses where context is provided upfront using default context builder or some other means.
Sometimes, we need to put context based on the current code path, like add user_id and email in login flow.
ErrorTracker comes with context manager that can be used for such use cases.

.. code::

    from error_tracker import flask_scope

    with flask_scope() as scope:
        scope.set_extra("user_id", 1234)
        scope.set_extra("email", "example@example.com" )


Now error_tracker will automatically capture exception as it will occur. This data will be stored in request_data detail as

.. code::

    {
       ...
        "context" : {
            "id" : 1234,
            "email" :  "example@example.com"
        }
    }