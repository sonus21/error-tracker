Ticketing
---------
Ticketing interface can be used to create tickets in the systems like Jira, Bugzilla etc, ticketing can be enabled using ticketing interface.

**Using TicketingMixin class**


implement raise_ticket method of TicketingMixin interface

.. code::

        from error_tracker import TicketingMixin
        class Ticketing(TicketingMixin):
            def raise_ticket(self, exception, request=None):
                # Put your logic here

Flask App Usage
===============

.. code::

    app = Flask(__name__)
    db = SQLAlchemy(app)
    error_tracker = AppErrorTracker(app=app, db=db, ticketing=Ticketing() )
    db.create_all()


Django App Usage
================
**settings.py**

.. code::

    APP_ERROR_TICKETING_MODULE = "path to Ticketing class"



