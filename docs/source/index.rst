.. flake8 documentation master file, created by
   sphinx-quickstart on Tue Jan 19 07:14:10 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=============================================================
Flask error/exception monitoring app
=============================================================

Quick start
==========

Installation
------------

To install Flask Error Monitor, open an interactive shell and run:

.. code::

    git clone git@github.com:sonus21/flask-error-monitor.git
    cd flask-error-monitor
    python setup.py install

User Guide
-----------
.. note::
  - It will mask all the variables which contain *password* and  *secret* in their name.
  - Recorded exceptions will be visible to *http://example.com/dev/error*

Using **Flask Error Monitor** as simple as plugging any flask extension. We need to create a new instance of *AppErrorManager* and configure that with the correct data.
You can use either object or app-based configuration, the only important thing here is we should have all the required key in the app.config dictionary to it to work.

Recording exception/error
^^^^^^^^^^^^^^^^^^^^^^^^^
An error/exception can be recorded using decorator as well function call.
- To record the error using decorator, decorate a function with *record_error_required*
- Where as to record error using function call use  *record_error* function.

All the data will be stored in the configured data store and these data will be available at */dev/error/*  or at configure URL path.


Example setup
---------------------------

For object based configuration add
**settings.py**

.. code::

    ...
    APP_ERROR_SEND_EMAIL = True
    APP_ERROR_RECIPIENT_EMAIL = ('example@example.com',)
    APP_ERROR_SUBJECT_PREFIX = "Server Error"
    APP_ERROR_EMAIL_SENDER = 'user@example.com'

**app.py**

.. code::

    from flask import Flask
    from flask_mail import Mail
    import settings
    from flask_error import AppErrorManager
    from flask_sqlalchemy import SQLAlchemy
    ...
    app = Flask(__name__)
    app.config.from_object(settings)
    db = SQLAlchemy(app)
    mail = Mail(app=app)
    error_manager = AppErrorManager(app=app, db=db, mailer=mail)

    ....

    ....
    # Record exception when 404 error code is raised
    @app.errorhandler(403)
    def error_403(e):
        error_manager.record_error()
        ...
        pass

    # Record error using decorator
    @app.errorhandler(500)
    @error_manager.record_error_required
    def error_500(e):
        ...
        pass
    ....

Here, app, db and mailer parameters are optional. Alternatively, you could use the init_app() method.

If you start this application and navigate to http://localhost:5000/dev/error, you should see an empty page.



Configure at the end
---------------------------
    Use error_manager.init method to configure

.. code::

    error_manager = AppErrorManager()
    ...
    error_manager.init_app(app=app, db=db, mailer=mail)


Config details
--------------
- Enable or disable email sending feature
   .. code::

     APP_ERROR_SEND_EMAIL = False
- Email recipient list
   .. code::

      APP_ERROR_RECIPIENT_EMAIL = None
- Email subject prefix to be used by email sender
   .. code::

      APP_ERROR_SUBJECT_PREFIX = ""

- Mask value with following string
    .. code::

      APP_ERROR_MASK_WITH = "**************"
- Mask rule
    App can mask all the variables whose lower case name contains one of the configured string
    .. code::

        APP_ERROR_MASKED_KEY_HAS = ("password", "secret")

    Above configuration will mask the variable names like
     .. code::

        password
        secret
        PassWord
        THis_Is_SEcret

    Any variable names whose lower case string contains either *password* or *secret*


- Browse link in your service app
    List of exceptions can be seen at */dev/error*, but you can have other prefix as well due to some securities or other reasons.
    .. code::

        APP_ERROR_URL_PREFIX = "/dev/error"

- Email error sender used to construct Message object
    .. code::

        APP_ERROR_EMAIL_SENDER = None


.. toctree::
    :maxdepth: 2

    Persistence Store <datastore>
    Email Sender <mail>
    Masking <mask-rule>

.. automodule::
    flask_error
