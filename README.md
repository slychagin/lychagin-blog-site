# My Blog
### Deployed on Heroku:
https://serhio-blog.herokuapp.com
### My first website written in Flask

The frontend of the website is based on the Bootstrap Clear Blog. Backend implemented in Flask.
The functionality of the site includes the following features:
- register a new user and save it into database;
- log in and log out;
- admin can post, edit and delete posts (all these operations are stored in the database);
- all registered users can leave comments under the posts, and also delete their own comments;
- on the contacts page, you can send your contact information to the mail of the site administrator.

### Website at work:

#### Site appierance.
![site_appiearance](https://github.com/slychagin/lychagin-blog-site/blob/master/gifs/Site%20appearance.gif)

#### Registration, log in, log out.
![registration_login](https://github.com/slychagin/lychagin-blog-site/blob/master/gifs/Registration%20and%20log%20in.gif)

#### Create, edit, delete post. Add comments.
![create_edit_delete_post](https://github.com/slychagin/lychagin-blog-site/blob/master/gifs/Create%20edit%20delete%20post.gif)

#### Send email to contact with site owner.
![send_email](https://github.com/slychagin/lychagin-blog-site/blob/master/gifs/Send%20email.gif)

### Technologies:
- Python 3, HTML, CSS;
- Flask, Flask WTF, Bootstrap;
- SQLAlchemy, Working with the database.

### You can run this project locally just do:
- `git clone https://github.com/slychagin/my-blog-site.git`;
- you must have Python 3 installed on your computer;
- install all requirements from requirements.txt;
- enter any secret key for Flask to work;
- `python main.py`;
- or go to https://serhio-blog.herokuapp.com
