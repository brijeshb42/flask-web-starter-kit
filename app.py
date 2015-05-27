import os
import logging
import sys
import string
import random

from flask import Flask, render_template, flash, url_for, \
    redirect, request
from werkzeug.security import generate_password_hash, \
    check_password_hash
from werkzeug.contrib.fixers import ProxyFix

from flask.ext.cache import Cache

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, \
    login_required, login_user, logout_user, current_user

from flask_wtf import Form
from wtforms import StringField, PasswordField, \
    BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, URL, \
    Length

from vomitter import DEFAULT_LOGGER as L
from config import config


__version__ = "0.1.0"
__author__ = "Brijesh Bittu <brijeshb42@gmail.com>"

"""User login management."""
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_message_category = "info"
login_manager.login_message = "You need to login."
login_manager.login_view = "login"


"""App setup."""
app = Flask(
        __name__,
        template_folder="templates/",
        static_url_path="/static",
        static_folder="templates/static/")
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)
app.config.from_object(config["default"])
login_manager.init_app(app)
cache = Cache(config={"CACHE_TYPE": "simple"})
cache.init_app(app)
logger = logging.Logger(config["default"].APP_NAME)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

"""DB Models."""


class AuthUser(db.Model, UserMixin):
    __tablename__ = "auth_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(40), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError(u"Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User %s>" % self.username or "None"

"""UI Forms."""


class LoginForm(Form):
    username = StringField(u"Username", validators=[
        DataRequired(message="Provide a username.")])
    password = PasswordField(u"Password", validators=[
        DataRequired(message="Provide a password.")])
    remember_me = BooleanField(u"Remember Me")


@login_manager.user_loader
def load_user(user_id):
    logging.debug("Querying users.")
    return AuthUser.query.get(int(user_id))


def get_random_part(length):
    """Get a random 5 letter string."""
    random_pad = "".join(
        random.choice(string.ascii_lowercase) for i in range(length))
    return random_pad


@app.route("/")
def index():
    return render_template(
        "index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthUser.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next", "") or
                            url_for("index"))
        flash(u"Invalid combination", "warning")
    return render_template("auth/login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
