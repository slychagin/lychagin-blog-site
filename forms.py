from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField


class CreatePostForm(FlaskForm):
    title = StringField('Заголовок поста', validators=[DataRequired(message='Это поле обязательно.')])
    subtitle = StringField('Подзаголовок', validators=[DataRequired(message='Это поле обязательно.')])
    img_url = StringField('Ссылка на фото', validators=[DataRequired(message='Это поле обязательно.'), URL()])
    body = CKEditorField('Содержание поста', validators=[DataRequired(message='Это поле обязательно.')])
    submit = SubmitField('Разместить пост')


class RegisterForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(message='Это поле обязательно.'),
                                             Email(message='Неверный почтовый адрес.')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле обязательно.'),
                                                     Length(min=8,
                                                            message='Пароль должен быть не менее 8-ми символов.')])
    name = StringField('Имя', validators=[DataRequired(message='Это поле обязательно.')])
    submit = SubmitField('Зарегистрировать!')


class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(message='Это поле обязательно.'), Email(message='Неверный почтовый адрес.')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле обязательно.'),
                                                     Length(min=8, message='Пароль должен быть не менее 8-ми символов.')])
    submit = SubmitField('Войти!')


class CommentForm(FlaskForm):
    comment_text = CKEditorField('Комментарий', validators=[DataRequired(message='Это поле обязательно.')])
    submit = SubmitField('Разместить комментарий')
