from flask import make_response
import json
import os
from lcoin_wallet.models import Request


def api_response(json_data: dict):
    resp = make_response(json.dumps(json_data))
    resp.content_type = "application/json; charset=utf-8"
    return resp

def get_secret_key():
    if os.path.exists(os.getcwd() + '/lcoin_wallet/config.ini'):
        import configparser
        config = configparser.ConfigParser()
        config.read(os.getcwd() + '/lcoin_wallet/config.ini')
        
        WHITELIST_SECRET = config['SERVER']['WHITELIST_SECRET']
    else:
        WHITELIST_SECRET = os.environ.get("WHITELIST_SECRET")
        
    return WHITELIST_SECRET

def check_if_pending(current_user):
    by_user = Request.query.filter_by(by=current_user.username, active=True)
    to_user = Request.query.filter_by(to=current_user.username, active=True)

    return [by_user.first() is not None, to_user.first() is not None], [by_user, to_user]