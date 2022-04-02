from flask import render_template, Blueprint

errors = Blueprint('error', __name__)

@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html", title='404 Error', e=e), 404

@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html", title='Server Error', e=e), 500