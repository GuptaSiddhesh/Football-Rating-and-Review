from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email,
                                EqualTo, ValidationError, Optional)
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, SelectField
import pyotp

from .models import User


class SearchForm(FlaskForm):
    search_query = SelectField('Team', choices=[('BAL', 'Baltimore Ravens'), ('BUF', 'Buffalo Bills'),('GB', 'Green Bay Packers'),
                                                ('HOU', 'Houston Texans'), ('KC', 'Kansas City Chiefs'),
                                                ('MIN', 'Minnesota Vikings'),
                                                ('NE', 'New England Patriots'), ('NO', 'New Orleans Saints'),
                                                ('NYJ', 'New York Jets'), ('PHI', 'Philadelphia Eagles'), ('SEA', 'Seattle Seahawks'),
                                                ('SF', 'San Francisco 49ers'), ('TEN', 'Tennessee Titans'),
                                                ('ALL', 'All Teams')])
    submit = SubmitField('Search')


class PlayerCommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired(), Length(min=1, max=500)])
    draftRound = IntegerField('Draft Round', validators=[InputRequired(), NumberRange(min=1, max=15,
                                                                                      message='Draft Round must be between 1 and 15')])
    playAgain = SelectField('Play Again', choices=[('YES', 'Yes'), ('NO', 'No')])
    submit = SubmitField('Submit Review')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
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


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])

    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()#To check if username already exists in database
        if user is None:
            raise ValidationError('Pleast Try Again')



class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])

    submit = SubmitField('Update Username')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')
