from datetime import datetime
import imp
from lcoin_wallet import db, login_manager
from flask_login import UserMixin

from itsdangerous import URLSafeTimedSerializer as Serializer

from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpeg')

    password = db.Column(db.String(60), nullable=False)

    balance = db.Column(db.Float, nullable=False)
    
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'],)
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token, expires_sec)['user_id']
        except:  
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    by = db.Column(db.String(20), nullable=False)

    to = db.Column(db.String(20), nullable=False)

    amount = db.Column(db.Float, nullable=False)
    
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    concept = db.Column(db.String(240), nullable=True)

    def __repr__(self):
        return f"Transaction('{self.date}', '{self.by}', '{self.to}', '{self.amount}', '{self.concept}')"

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    by = db.Column(db.String(20), nullable=False)

    to = db.Column(db.String(20), nullable=False)

    amount = db.Column(db.Float, nullable=False)
    
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    concept = db.Column(db.String(240), nullable=True)

    active = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return f"Request('{self.date}', '{self.by}', '{self.to}', '{self.amount}', '{self.concept}')"
    
class EmailWhitelist(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    
    initial_balance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"EmailWhitelist('{self.id}', '{self.email}', '{self.initial_balance}')"