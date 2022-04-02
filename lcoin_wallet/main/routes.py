from flask import render_template, url_for, redirect
from lcoin_wallet.main.utils import check_if_pending, get_transactions
from flask_login import login_required, current_user
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    exists, _ = check_if_pending(current_user)
    transactions = get_transactions(current_user)

    if exists[1] is True:
        notification = "badge1"
    else:
        notification = None

    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)

    if len(transactions) > 1:
        return render_template("index.html", title='Wallet', image_file=image_file, notification=notification, transactions=transactions[::-1])
    else:
        return render_template("index.html", title='Wallet', image_file=image_file, notification=notification, transactions=[])


@main.route('/error_500')
def error_500():
    error = "Internal server error has been detected...Internal server error has been detected...Internal server"
    return render_template("500.html", e=error)