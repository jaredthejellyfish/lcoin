from flask import render_template, url_for, redirect
from lcoin_wallet.main.utils import (
    check_if_pending, get_transactions, transaction_html_constructor, get_btc_price)
from flask_login import login_required, current_user
from flask import Blueprint, send_from_directory


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    exists, _ = check_if_pending(current_user)
    transactions = get_transactions(current_user)
    btc_price = round(get_btc_price(), 6)
    transactions_html = transaction_html_constructor(transactions, btc_price)
    
    if exists[1] is True:
        notification = "badge1"
    else:
        notification = None

    image_file = url_for('main.profile_photo')

    if len(transactions) > 1:
        return render_template("index.html", title='Wallet', image_file=image_file, notification=notification, transactions_html=transactions_html, btc_price=btc_price)
    else:
        return render_template("index.html", title='Wallet', image_file=image_file, notification=notification, transactions=[])


@main.route('/sw.js')
def sw():
    return send_from_directory('static', 'sw.js')


@main.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')


@main.route('/app/static/js')
def app_js():
    return send_from_directory('static', 'javascript/app.js')


@main.route('/l-coin-logo.png')
def logo():
    return send_from_directory('static', 'images/l-coin-logo.png')


@main.route('/profile_photo')
def profile_photo():
    return send_from_directory('static', f'profile_pics/{current_user.image_file}')


@main.route('/error_500')
def error_500():
    error = "Internal server error has been detected...Internal server error has been detected...Internal server"
    return render_template("errors/500.html", e=error)