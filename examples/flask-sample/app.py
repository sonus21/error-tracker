from flask import Flask
from flask import render_template
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

import settings
from error_tracker import AppErrorTracker, NotificationMixin, TicketingMixin


class Notifier(Mail, NotificationMixin):
    def __init__(self, *args, **kwargs):
        Mail.__init__(self, *args, **kwargs)
        NotificationMixin.__init__(self, *args, **kwargs)

    def notify(self, request, exception,
               email_subject=None,
               email_body=None,
               from_email=None,
               recipient_list=None):
        message = Message(email_subject, recipient_list, email_body, sender=from_email)
        self.send(message)


class Ticketing(TicketingMixin):
    def raise_ticket(self, exception, request=None):
        # implement this method to communicate with Jira or Bugzilla etc
        pass


app = Flask(__name__)
app.config.from_object(settings)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask.sqlite"
db = SQLAlchemy(app)

app_error = AppErrorTracker(app=app, db=db,
                            notifier=Notifier(app=app),
                            ticketing=Ticketing())
db.create_all()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/go')
def die():
    import random
    password = "test"
    foo = {}
    foo['password'] = "Oh! My Gosh"
    foo['secret'] = "NO ONE KNOWS"
    exceptions = [KeyError, ArithmeticError, BaseException, IndentationError, IndexError, MemoryError,
                  NameError, NotImplementedError, ImportError, FloatingPointError, EOFError,
                  OSError, AssertionError, AttributeError, GeneratorExit, Exception,
                  EnvironmentError, ImportError,
                  NotImplementedError, RuntimeError]
    raise random.choice(exceptions)


@app.errorhandler(401)
def error_401(e):
    app_error.capture_exception()
    return render_template('401.html'), 401


@app.errorhandler(500)
@app_error.track_exception
def error_500(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=False)
