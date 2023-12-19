"""This file contains the registration page"""

from datetime import date
import bcrypt
from flask import Blueprint, request, redirect, render_template, url_for
import flask_login
from markupsafe import escape
import sqlalchemy

from app import app, db
from app.models import User
from app.user import calculate_age

register_bp = Blueprint("register", __name__)


@app.route("/", methods=["GET", "POST"])
def register():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("dating"), code=302)

    error = None

    if request.method == "POST":
        username = escape(request.form.get("username"))
        first_name = escape(request.form.get("first_name"))
        birth_date = None
        try:
            birth_date = date.fromisoformat(request.form.get("birth_date"))
            if calculate_age(birth_date) < 18:
                error = "Users younger than 18 are not allowed."
        except (TypeError, ValueError):
            error = "Incorrect date value."
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if not error:
            if (
                username
                and first_name
                and birth_date
                and email
                and password
                and confirm
            ):
                if password == confirm:
                    try:
                        db.session.add(
                            User(
                                username=username,
                                first_name=first_name,
                                birth_date=birth_date,
                                email=email,
                                password=bcrypt.hashpw(
                                    password.encode(), bcrypt.gensalt()
                                ).decode(),
                            )
                        )
                        db.session.commit()
                    except sqlalchemy.exc.IntegrityError:
                        error = "Username already taken."
                else:
                    error = "Invalid password confirmation."
            else:
                error = "Some required data is missing."
        if not error:
            user = db.session.query(User).filter_by(username=username).first()
            flask_login.login_user(user)
            return redirect("/dating", code=302)

    return render_template("register.html", error=error)
