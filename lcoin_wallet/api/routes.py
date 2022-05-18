from sqlalchemy import func

from lcoin_wallet import db
from lcoin_wallet.models import Request, User, Transaction

import flask

from lcoin_wallet.models import User, Transaction, Request, EmailWhitelist

from lcoin_wallet.api.utils import api_response, get_secret_key,check_if_pending

from flask_login import current_user, login_required

from flask import Blueprint

api = Blueprint('api', __name__)


@api.route("/api/accept_request/", methods=["GET"])
def accept_request():

    args = flask.request.args.to_dict()

    if args["key"]:
        try:
            request = Request.query.filter_by(id=args["key"]).first()

            to = User.query.filter(func.lower(
                User.username) == func.lower(request.to)).first()
            by = User.query.filter(func.lower(
                User.username) == func.lower(request.by)).first()

            if to.balance < request.amount:
                request.active = False
                db.session.commit()
                return api_response({"state": "error"})

            transaction = Transaction(by=request.to,
                                      to=request.by,
                                      amount=request.amount,
                                      concept=request.concept)

            by.balance += request.amount
            to.balance -= request.amount

            request.active = False

            db.session.add(transaction)

            db.session.commit()

            return api_response({"state": "success", "amount": request.amount, "username": request.by})
        except:
            return api_response({"state": "error"})


@api.route("/api/deny_request/", methods=["GET"])
def deny_request():
    args = flask.request.args.to_dict()

    if args["key"]:
        try:
            request = Request.query.filter_by(id=args["key"]).first()

            request.active = False

            db.session.commit()

            return api_response({"state": "success", "amount": request.amount, "username": request.by})
        except:
            return api_response({"state": "error"})


@api.route("/api/add_email/<secret>/<email>/<start_balance>", methods=["GET"])
def add_email(secret, email, start_balance):
    print(email, start_balance)
    try:
        key = get_secret_key()
        
        if secret == key:
            email = EmailWhitelist(email=email, initial_balance=start_balance)
            db.session.add(email)
            db.session.commit()
            return api_response({"state": "success"})
        else:
            return api_response({"state": "unauthorized"})
    except:
        return api_response({"state": "error"})

@api.route("/api/pending_requests", methods=["GET"])
@login_required
def pending_request():
    exists, _ = check_if_pending(current_user)
    
    if exists[1] is True:
        return api_response({"notification_badge": "true"})
    else:
        return api_response({"notification_badge": "false"})
    
    #http://10.10.20.57:8080/api/add_email/Holalola123/ger.almenara@gmail.com/41