from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField


class CreatePostForm(FlaskForm):
    title = StringField('Blog Post Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Your Name', validators=[DataRequired()])
    img_url = StringField('Blog Image URL', validators=[DataRequired(), URL()])
    body = CKEditorField('Blog Content', validators=[DataRequired()])
    submit = SubmitField('Submit Post')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Invalid email address.')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8,
                                                            message='Field must be at least 8 characters long.')])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Sign Me Up!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email address.')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, message='Field must be at least 8 characters long.')])
    submit = SubmitField('Let Me In!')
