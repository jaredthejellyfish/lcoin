from flask import render_template

def page_not_found(e):
    return render_template("404.html", title='404 Error', e=e)

def internal_server_error(e):
    return render_template("500.html", title='Server Error', e=str(e))