from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from lcoin_wallet.error_handlers import page_not_found
import os 

app = Flask(__name__)

app.config['SECRET_KEY'] = '5e971d11505ed2faf96da8341de6f576aac555865d35d9f465f9073636ba46a8'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_error_handler(404, page_not_found)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from lcoin_wallet import routes