from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from chatb.models import User

def check_credentials(form, field):
    ''' Custom validator for checking the credentials on login '''
    username_entered = form.username.data
    password_entered = field.data
    user_obj = User.query.filter_by(username = username_entered).first()
    if user_obj is None or user_obj.password != password_entered:
        raise ValidationError("Invalild username or password.")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="You must create a username."),
                                                   Length(min=4, max=25, message="Username should be between 4 and 25 characters.")])
    password = PasswordField("Password", validators=[InputRequired(message="You must create a password.")])
    signup_btn = SubmitField("Sign Up")

    def validate_username(self, username):
        user_obj = User.query.filter_by(username=username.data).first()
        if(user_obj):
            raise ValidationError("Username already exists.")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), check_credentials])
    login_btn = SubmitField("Login")
