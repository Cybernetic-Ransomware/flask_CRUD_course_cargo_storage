from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from storage.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist, please try different one.')

    def validate_email_address(self, email_to_check):
        email = User.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('E-mail address already in usage.')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='E-mail address:', validators=[Email(), DataRequired()])
    password_01 = PasswordField(label='New password:', validators=[Length(min=6), DataRequired()])
    password_02 = PasswordField(label='Confirm password:', validators=[EqualTo('password_01'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PossessItemForm(FlaskForm):
    submit = SubmitField(label='Possess Item!')


class ReturnItemForm(FlaskForm):
    submit = SubmitField(label='Return Item!')
