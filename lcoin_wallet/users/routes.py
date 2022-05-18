import os
from sqlalchemy import func

from lcoin_wallet import db, bcrypt
from lcoin_wallet.models import User, Transaction
from lcoin_wallet.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                      RequestResetForm,
                                      ResetPasswordForm)

from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint, current_app)
import flask

from lcoin_wallet.models import User, Transaction, EmailWhitelist

from flask_login import login_required, login_user, current_user, logout_user

from lcoin_wallet.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            prev_picture = os.path.join(
                current_app.root_path, 'static/profile_pics', current_user.image_file)
            if os.path.exists(prev_picture) and current_user.image_file != "default.jpeg":
                os.remove(prev_picture)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        if current_user.username != form.username.data:
            transactions_by = Transaction.query.filter_by(
                by=current_user.username)

            for transaction in transactions_by:
                transaction.by = form.username.data

            transactions_to = Transaction.query.filter_by(
                to=current_user.username)

            for transaction in transactions_to:
                transaction.to = form.username.data

            db.session.commit()

        current_user.username = form.username.data

        if EmailWhitelist.query.filter(func.lower(User.email) == func.lower(form.email.data)).first():
            current_user.email = form.email.data

        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    elif flask.request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    new_user_exists = User.query.filter(func.lower(User.username) == func.lower(
        form.username.data), func.lower(User.email) == func.lower(form.email.data)).first()
    if new_user_exists:
        flash(
            f'Welcome {new_user_exists.username}! Looks like you are already registered, please log in!', 'success')
        return redirect(url_for('users.login'))

    if form.validate_on_submit():
        whitelist_entry = EmailWhitelist.query.filter_by(email=form.email.data).first()
        if whitelist_entry:
            hashed_passoword = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            
            user = User(username=form.username.data,
                        email=form.email.data, password=hashed_passoword, balance=whitelist_entry.initial_balance)
            
            transaction = Transaction(by="LCoin",
                                      to=form.username.data,
                                      amount=whitelist_entry.initial_balance,
                                      concept="Welcome to LCoin, here is the balance you had in the last marketplace!")
            db.session.add(user)
            db.session.add(transaction)
            db.session.commit()
            flash(
                f'Welcome {user.username}! You can now use your credentials to log in.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(
                f'Sorry but that email is not in our list!', 'danger')

    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.username) == func.lower(
            form.email_or_username.data)).first()
        if not user:
            user = User.query.filter(func.lower(User.email) == func.lower(
                form.email_or_username.data)).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            try:
                next_page = request.args.get('next')
            except AttributeError:
                next_page = None

            flash(f'Welcome {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login unsuccessfull, please check email and password...', 'danger')

    return render_template("login.html", title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/reset_password',  methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            f'An email has been sent to {form.email.data} with instructions to reset your password!', 'success')
        return redirect(url_for('users.login'))

    return render_template("reset_request.html", title='Reset Password', form=form)


@users.route('/reset_password/<token>',  methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)

    if not user:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_passoword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        user.password = hashed_passoword

        db.session.commit()

        flash(
            f'{user.username}, your password has been reset successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template("users.reset_token.html", title='Reset Password', form=form)
