from flask import make_response
import json

def api_response(json_data: dict):
    resp = make_response(json.dumps(json_data))
    resp.content_type = "application/json; charset=utf-8"
    return resp
