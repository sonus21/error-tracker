Email send feature
----------------------------

Emails can be send using different method instead of standard flask Mail; to do that you have to implement **send** method from *MailMixin* as

.. code::

       from flask_error import MailMixin
       class TestMail(MailMixin):
            emails = []

            def send(self, message):
                # Put what ever logic you want here
                self.emails.append(message)

       ...
       # create app
       error_manager = AppErrorManager(app=app, db=db, mail=TestMail())
       ...



