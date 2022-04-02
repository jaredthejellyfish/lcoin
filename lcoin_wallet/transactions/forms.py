from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length

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
