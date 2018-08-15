from flask import Flask
from flask import render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

import settings
from flask_error import AppErrorManager

app = Flask(__name__)
app.config.from_object(settings)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp.sqlite"
db = SQLAlchemy(app)
mail = Mail(app=app)
app_error = AppErrorManager(app=app, db=db,  url_prefix="/dev/exception")
db.create_all()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/go')
def hello_world():
    password = "test"
    foo = {}
    foo['password'] = "ME"
    foo['secret'] = "ME"
    raise ArithmeticError()
    return 'Hello World!'


@app.errorhandler(403)
def error_403(e):
    app_error.record_error()
    return render_template('403.html'), 403


@app.errorhandler(500)
@app_error.record_error_required
def error_500(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=False)
