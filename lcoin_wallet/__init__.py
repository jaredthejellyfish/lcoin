import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from lcoin_wallet.error_handlers import page_not_found, internal_server_error

from flask_minify import Minify

import os 

app = Flask(__name__)

if os.path.exists(os.getcwd() + '/lcoin_wallet/config.ini'):
    import configparser
    config = configparser.ConfigParser()
    config.read(os.getcwd() + '/lcoin_wallet/config.ini')
    app.config['SECRET_KEY'] = config['SERVER']['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = config['SERVER']['DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = config['EMAIL']['EMAIL_USER']
    app.config['MAIL_PASSWORD'] = config['EMAIL']['EMAIL_PASS']

else:
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace("postgres", "postgresql")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

Minify(app=app, html=True, js=True, cssless=True)

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

from lcoin_wallet import routes