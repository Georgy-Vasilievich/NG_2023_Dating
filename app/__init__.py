"""Dating website, main file"""

import os
import threading

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_login
import sqlalchemy

from config import Config, send_emails

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, mail, models
from app.models import User

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(user_id):
    try:
        return db.session.query(User).filter_by(id=user_id).first()
    except Exception as e:
        print(f"Exception: {e}")


if not os.path.isdir(os.path.join("app", "static", "avatars")):
    os.mkdir(os.path.join("app", "static", "avatars"))


if send_emails:
    mail_thread = threading.Thread(
        target=mail.mail_sender, args=(app.app_context(),), daemon=True
    )
    mail_thread.start()
