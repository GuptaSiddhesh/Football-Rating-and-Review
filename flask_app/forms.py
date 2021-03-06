from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email,
                                EqualTo, ValidationError, Optional)
from wtforms_validators import AlphaNumeric, Alpha
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, SelectField
import pyotp

from .models import User


class SearchForm(FlaskForm):
    search_query = SelectField('Team', choices=[('BAL', 'Baltimore Ravens'), ('BUF', 'Buffalo Bills'),('GB', 'Green Bay Packers'),
                                                ('HOU', 'Houston Texans'), ('KC', 'Kansas City Chiefs'),
                                                ('MIN', 'Minnesota Vikings'),
                                                ('NE', 'New England Patriots'), ('NO', 'New Orleans Saints'),
                                                ('PHI', 'Philadelphia Eagles'), ('SEA', 'Seattle Seahawks'),
                                                ('SF', 'San Francisco 49ers'), ('TEN', 'Tennessee Titans'),
                                                ('ALL', 'All Teams')])
    submit = SubmitField('Search')


class PlayerCommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired(), Length(min=1, max=500),
                                                Alpha(message='Comment must contain only alphabets')])
    draftRound = IntegerField('Suggest a Draft Round', validators=[InputRequired(), NumberRange(min=1, max=15,
                                                                    message='Draft Round must be between 1 and 15')])
    rating = IntegerField('Provide a rating between 1-10', validators=[InputRequired(), NumberRange(min=1, max=10,
                                                                                                    message='Rating must be between 1 and 10')])
    playAgain = SelectField('Would you play this player again?', choices=[('YES', 'Yes'), ('NO', 'No')])
    submit = SubmitField('Submit Review')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40),
                                                   AlphaNumeric(message='Username must contain only alphabets and numbers only')])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=10, max=20, message="Minimum length 10 for strong password")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username has already been used')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Email has already been used')

class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20),
                                                   AlphaNumeric(message='Username must contain only alphabets and numbers only')])

    submit = SubmitField('Update Username')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])

    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()#To check if username already exists in database
        if user is None:
            raise ValidationError('Pleast Try Again')




