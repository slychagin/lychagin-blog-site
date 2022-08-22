import datetime
import smtplib
import bleach
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from functools import wraps

my_email = 'slychagin@yahoo.com'
password = 'tppqvaywjyegvgfd'

app = Flask(__name__)
app.config['SECRET_KEY'] = '5a01beb4fb2a01c4c2ff2a8308409c5669b2eb19f414c314d24fb3893920c10a'
ckeditor = CKEditor(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False,
                    base_url=None)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# DECORATOR FOR FORBIDDEN PAGES
def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_anonymous or current_user.id != 1:
            return abort(403)
        return function(*args, **kwargs)
    return wrapper


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE blog_post TABLE
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship('Comment', back_populates='parent_post')


# CREATE the User TABLE
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    name = db.Column(db.String(250))
    posts = relationship('BlogPost', back_populates='author')
    comments = relationship('Comment', back_populates='comment_author')


# CREATE COMMENTS TABLE
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_author = relationship('User', back_populates='comments')
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    parent_post = relationship('BlogPost', back_populates='comments')
    text = db.Column(db.Text, nullable=False)


# db.create_all()


# Strips invalid tags/attributes
def strip_invalid_html(content):
    allowed_tags = ['a', 'abbr', 'acronym', 'address', 'b', 'br', 'div', 'dl', 'dt',
                    'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                    'li', 'ol', 'p', 'pre', 'q', 's', 'small', 'strike',
                    'span', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                    'thead', 'tr', 'tt', 'u', 'ul']
    allowed_attrs = {
        'a': ['href', 'target', 'title'],
        'img': ['src', 'alt', 'width', 'height'],
    }
    cleaned = bleach.clean(content,
                           tags=allowed_tags,
                           attributes=allowed_attrs,
                           strip=True)
    return cleaned


# RENDER HOME PAGE USING DB
@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', all_posts=posts)


# CREATE NEW USER
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form.get('email')).first()

        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            email=request.form.get('email'),  # type: ignore
            password=hash_and_salted_password,  # type: ignore
            name=request.form.get('name')  # type: ignore
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('get_all_posts'))
    return render_template("register.html", form=form)


# LOG IN USER
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form.get('email')).first()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, request.form.get('password')):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template('login.html', form=form)


# LOG OUT USER
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


# RENDER POST USING DB
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def read_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                author_id=current_user.id,
                post_id=requested_post.id,
                text=strip_invalid_html(request.form.get('comment_text'))
            )
            db.session.add(new_comment)
            db.session.commit()
            form.comment_text.data = ""
        else:
            flash("You need to login or register to comment.")
            return redirect(url_for('login'))
    return render_template('post.html', form=form, post=requested_post)


# CREATE NEW POST
@app.route('/new-post', methods=['GET', 'POST'])
@admin_only
@login_required
def add_new_post():
    form = CreatePostForm()
    blog_post_date = datetime.datetime.now().strftime('%B %d, %Y')
    if form.validate_on_submit():
        new_post = BlogPost(
            title=request.form.get('title'),
            subtitle=request.form.get('subtitle'),
            author_id=current_user.id,
            img_url=request.form.get('img_url'),
            body=strip_invalid_html(request.form.get('body')),
            date=blog_post_date
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=form)


# EDIT POST
@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
@admin_only
@login_required
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = request.form.get('title')
        post.subtitle = request.form.get('subtitle')
        post.img_url = request.form.get('img_url')
        post.body = request.form.get('body')
        db.session.commit()
        return redirect(url_for('read_post', post_id=post.id))
    return render_template('make-post.html', form=edit_form, is_edit=True)


# DELETE POST
@app.route('/delete/<int:post_id>')
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


# DELETE COMMENT
@app.route('/delete-comment/<int:post_id>/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(post_id, comment_id):
    comment_to_delete = Comment.query.get(comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for('read_post', post_id=post_id))


# RENDER ABOUT PAGE
@app.route('/about')
def about_page():
    return render_template('about.html')


# RENDER CONTACT PAGE
@app.route('/contact')
def contact_page():
    return render_template('contact.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        send_email(data['name'], data['email'], data['phone'], data['message'])
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


def send_email(name, email, phone, message):
    """
    This function send message on admin email
    :param name: User name
    :param email: User email
    :param phone: User phone
    :param message: User's message
    :return: None
    """
    with smtplib.SMTP('smtp.mail.yahoo.com', port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs='lychagin.sergey@mail.ru',
                            msg=f'Subject: Message from my blog\n\n'
                                f'Name: {name}\n'
                                f'Email: {email}\n'
                                f'Phone: {phone}\n'
                                f'Message: {message}'.encode('utf-8')
                            )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
