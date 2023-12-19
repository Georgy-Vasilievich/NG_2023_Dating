"""This file contains the login page"""

import bcrypt
from flask import Blueprint, request, redirect, render_template, url_for
import flask_login

from app import app, db
from app.models import User

login_bp = Blueprint("login", __name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("dating"), code=302)

    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            user = db.session.query(User).filter_by(username=username).first()
            if user and bcrypt.checkpw(password.encode(), user.password.encode()):
                flask_login.login_user(user)
                redirect_path = request.args.get("next")
                return redirect(redirect_path if redirect_path else "/dating", code=302)
            error = "Incorrect data."
        except Exception as e:
            print(f"Exception: {e}")

    return render_template("login.html", error=error)
