from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lcoin_wallet.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired()], id='password')
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')], id='confirm-password')

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken, please choose a different one...')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already in use...')


class LoginForm(FlaskForm):
    email_or_username = StringField('Email or Username',
                                    validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired()], id='password')
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken, please choose a different one...')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already in use...')


class SendMoneyForm(FlaskForm):
    to = StringField('Username',
                     validators=[DataRequired(), Length(min=2, max=20)])

    concept = TextAreaField('Concept', validators=[Length(max=241)])

    amount = FloatField('Amount', validators=[DataRequired()])

    submit = SubmitField('Send')


class RequestMoneyFrom(FlaskForm):
    to = StringField('Username',
                     validators=[DataRequired(), Length(min=2, max=20)])

    concept = TextAreaField('Concept', validators=[Length(max=241)])

    amount = FloatField('Amount', validators=[DataRequired()])

    submit = SubmitField('Send')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(
                'There is no account with this email. You must register first...')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
                             DataRequired()], id='password')

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')], id='confirm-password')


    submit = SubmitField('Reset Password')
