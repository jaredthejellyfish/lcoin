from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from flask_minify import Minify

from lcoin_wallet.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @app.after_request
    def apply_nocache(response):
        response.headers["Cache-Control"] = "no-cache"
        return response

    from lcoin_wallet.users.routes import users
    from lcoin_wallet.transactions.routes import transactions
    from lcoin_wallet.main.routes import main
    from lcoin_wallet.api.routes import api
    from lcoin_wallet.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(transactions)
    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(errors)

    Minify(app=app, html=True, js=True, cssless=True)

    return app

