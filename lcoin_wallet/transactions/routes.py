from sqlalchemy import func

from lcoin_wallet import db
from lcoin_wallet.models import Request, User, Transaction
from lcoin_wallet.transactions.forms import SendMoneyForm, RequestMoneyFrom
from flask import render_template, url_for, flash, redirect
import flask

from lcoin_wallet.models import User, Transaction, Request

from flask_login import login_required, current_user

from flask import Blueprint

from lcoin_wallet.transactions.utils import get_sent, check_if_pending

transactions = Blueprint('transactions', __name__)


@transactions.route('/send', methods=['GET', 'POST'])
@login_required
def send():

    transactions = get_sent(current_user)

    form = SendMoneyForm()
    if form.validate_on_submit():
        to_user = User.query.filter(func.lower(
            User.username) == func.lower(form.to.data)).first()
        if to_user:
            if current_user.username == to_user.username:
                flash('You cannot send money to yourself!', 'danger')
                return redirect(url_for('transactions.send'))
            elif current_user.balance < form.amount.data:
                flash('You don\'t have enough money to do that... :/', 'danger')
                return redirect(url_for('transactions.send'))
            else:
                transaction = Transaction(by=current_user.username,
                                          to=to_user.username,
                                          amount=form.amount.data,
                                          concept=form.concept.data)
                if form.amount.data > 0:
                    current_user.balance -= form.amount.data
                    to_user.balance += form.amount.data

                    db.session.add(transaction)
                    db.session.commit()

                    flash(
                        f'Succesfully sent ₺{form.amount.data} to {to_user.username}!', 'success')
                    return redirect(url_for('main.home'))

                else:
                    flash(
                        f'You cannot send negative money.', 'danger')
                    return redirect(url_for('main.home'))

        else:
            flash(
                f'{form.to.data} is not registered as a user in our database...', 'danger')
            return redirect(url_for('transactions.send'))

    return render_template("send.html", title='Send', form=form, requests=transactions.all()[::-1])


@transactions.route('/request',  methods=['GET', 'POST'])
@login_required
def request():
    args = flask.request.args.to_dict()

    try:
        if args['s'] == 'error':
            flash(
                f'Error processing your request, the user does not have enough funds...', 'danger')
            return redirect(url_for('transactions.request'))
        elif args["u"] and args['a'] and args['s'] == 'accept':
            flash(f'Succesfully sent ₺{args["a"]} to {args["u"]}!', 'success')
            return redirect(url_for('transactions.request'))
        elif args["u"] and args['a'] and args['s'] == 'deny':
            flash(f'Denied {args["u"]}\'s request for ₺{args["a"]}!', 'danger')
            return redirect(url_for('transactions.request'))
    except KeyError:
        pass

    form = RequestMoneyFrom()
    if form.validate_on_submit():
        to_user = User.query.filter(func.lower(
            User.username) == func.lower(form.to.data)).first()
        if to_user:
            if current_user.username == to_user.username:
                flash('You cannot request money from yourself!', 'danger')
                return redirect(url_for('transactions.request'))
            else:
                if form.amount.data > 0:
                    request = Request(by=current_user.username,
                                      to=to_user.username,
                                      amount=form.amount.data,
                                      concept=form.concept.data,
                                      active=True)

                    db.session.add(request)
                    db.session.commit()

                    flash(
                        f'Succesfully sent a request for ₺{form.amount.data} to {to_user.username}!', 'success')
                    return redirect(url_for('transactions.request'))

                else:
                    flash(
                        f'{form.to.data} is not registered as a user in our database...', 'danger')
                    return redirect(url_for('transactions.send'))

        else:
            flash(
                f'{form.to.data} is not registered as a user in our database...', 'danger')
            return redirect(url_for('transactions.request'))

    _, data = check_if_pending(current_user)
    _, to = data

    return render_template("request.html", title='Request', requests=to.all(), form=form)
