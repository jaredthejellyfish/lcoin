import secrets
import os
import json
from weakref import KeyedRef

from lcoin_wallet import app, db, bcrypt
from lcoin_wallet.models import Request, User, Transaction
from lcoin_wallet.forms import RegistrationForm, LoginForm, UpdateAccountForm, SendMoneyForm, RequestMoneyFrom

from flask import render_template, url_for, flash, redirect, request, make_response
import flask

from lcoin_wallet.models import User, Transaction, Request

from flask_login import login_required, login_user, current_user, logout_user

from PIL import Image

from lcoin_wallet.resize_image import resize_image

def check_if_pending(current_user):
    by_user = Request.query.filter_by(by=current_user.username, active=True)
    to_user = Request.query.filter_by(to=current_user.username, active=True)

    return [by_user.first() is not None, to_user.first() is not None], [by_user, to_user]

def get_sent(current_user):
    sent = Transaction.query.filter_by(by=current_user.username)

    return sent

def get_transactions(current_user):
    sent = []
    received = []

    sent_ = Transaction.query.filter_by(by=current_user.username)
    received_ = Transaction.query.filter_by(to=current_user.username)

    for transaction in sent_:
        sent.append(["Sent",transaction.date, transaction.to, transaction.amount])
    
    for transaction in received_:
        received.append(["Received", transaction.date, transaction.by, transaction.amount])

    lists = sorted(sent + received, key=lambda x:x[1])

    return lists
     

@app.route('/')
@app.route('/home')
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    exists, _ = check_if_pending(current_user)
    transactions = get_transactions(current_user)

    if exists[1] is True:
        notification = "badge1"
    else:
        notification = None

    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)

    if len(transactions ) > 1:
        return render_template("index.html", title='Wallet', image_file=image_file, notification=notification, transactions=transactions[::-1])
    else:
        return render_template("index.html", title='Wallet', image_file=image_file, notification=notification, transactions=[])



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)

    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    i = Image.open(form_picture)
    i = resize_image(i, 125)

    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            prev_picture = os.path.join(
                app.root_path, 'static/profile_pics', current_user.image_file)
            if os.path.exists(prev_picture) and current_user.image_file != "default.jpeg":
                os.remove(prev_picture)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif flask.request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    new_user_exists = User.query.filter_by(
        username=form.username.data, email=form.email.data).first()
    if new_user_exists:
        flash(
            f'Welcome {form.username.data}! Looks like you are already registered, please log in!', 'success')
        return redirect(url_for('login'))

    if form.validate_on_submit():
        hashed_passoword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_passoword)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Welcome {form.username.data}! You can now use your credentials to log in.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            try:
                next_page = request.args.get('next')
            except AttributeError:
                next_page = None

            flash(f'Welcome {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessfull, please check email and password...', 'danger')

    return render_template("login.html", title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/send', methods=['GET', 'POST'])
@login_required
def send():

    transactions = get_sent(current_user)

    form = SendMoneyForm()
    if form.validate_on_submit():
        to_user = User.query.filter_by(username=form.to.data).first()
        if to_user:
            if current_user.username == to_user.username:
                flash('You cannot send money to yourself!', 'danger')
                return redirect(url_for('send'))
            elif current_user.balance < form.amount.data:
                flash('You don\'t have enough money to do that... :/', 'danger')
                return redirect(url_for('send'))
            else:
                transaction = Transaction(by=current_user.username,
                                          to=form.to.data,
                                          amount=form.amount.data,
                                          concept=form.concept.data)

                current_user.balance -= form.amount.data
                to_user.balance += form.amount.data

                db.session.add(transaction)
                db.session.commit()

                flash(
                    f'Succesfully sent ₺{form.amount.data} to {form.to.data}!', 'success')
                return redirect(url_for('home'))

        else:
            flash(
                f'{form.to.data} is not registered as a user in our database...', 'danger')
            return redirect(url_for('send'))

    return render_template("send.html", title='Send', form=form, requests=transactions.all()[::-1])


@app.route('/request',  methods=['GET', 'POST'])
@login_required
def request():
    args = flask.request.args.to_dict()

    try:
        if args["u"] and args['a'] and args['s'] == 'accept':
            flash(f'Succesfully sent ₺{args["a"]} to {args["u"]}!', 'success')
            return redirect(url_for('request'))
        elif args["u"] and args['a'] and args['s'] == 'deny':
            flash(f'Denied {args["u"]}\'s request for ₺{args["a"]}!', 'danger')
            return redirect(url_for('request'))
    except KeyError:
        pass
    
    form = RequestMoneyFrom()
    if form.validate_on_submit():
        to_user = User.query.filter_by(username=form.to.data).first()
        if to_user:
            if current_user.username == to_user.username:
                flash('You cannot request money from yourself!', 'danger')
                return redirect(url_for('send'))
            else:
                request = Request(by=current_user.username,
                                          to=form.to.data,
                                          amount=form.amount.data,
                                          concept=form.concept.data,
                                          active=True)

                db.session.add(request)
                db.session.commit()

                flash(
                    f'Succesfully sent a request for ₺{form.amount.data} to {form.to.data}!', 'success')
                return redirect(url_for('request'))

        else:
            flash(
                f'{form.to.data} is not registered as a user in our database...', 'danger')
            return redirect(url_for('request'))

    _, data = check_if_pending(current_user)
    _, to = data

    return render_template("request.html", title='Request', requests=to.all(), form=form)


def api_response(json_data: dict):
    resp = make_response(json.dumps(json_data))
    resp.content_type = "application/json; charset=utf-8"
    return resp


@app.route("/api/accept_request/", methods=["GET"])
def accept_request():

    # Make a js function that takes input from a button, makes the api call, and then reloads the page!

    args = flask.request.args.to_dict()

    if args["key"]:
        try:
            request = Request.query.filter_by(id=args["key"]).first()

            to = User.query.filter_by(username=request.to).first()
            by = User.query.filter_by(username=request.by).first()

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

@app.route("/api/deny_request/", methods=["GET"])
def deny_request():

    # Make a js function that takes input from a button, makes the api call, and then reloads the page!

    args = flask.request.args.to_dict()

    if args["key"]:
        try:
            request = Request.query.filter_by(id=args["key"]).first()

            request.active = False

            db.session.commit()

            return api_response({"state": "success", "amount": request.amount, "username": request.by})
        except:
            return api_response({"state": "error"})