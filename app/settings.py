"""This file contains the settings page"""

from datetime import date
import bcrypt
from flask import Blueprint, request, redirect, render_template
import flask_login
from markupsafe import escape
import os

from app import app, db
from app.models import User
from app.user import calculate_age

settings_bp = Blueprint("settings", __name__)


@app.route("/settings", methods=["GET", "POST"])
@flask_login.login_required
def settings():
    error = None

    user = db.session.query(User).get(flask_login.current_user.id)

    if request.method == "POST":
        first_name = escape(request.form.get("first_name"))
        birth_date = None
        try:
            birth_date = date.fromisoformat(request.form.get("birth_date"))
            if calculate_age(birth_date) < 18:
                error = "Users younger than 18 are not allowed."
        except (TypeError, ValueError):
            pass
        email = escape(request.form.get("email"))
        location = escape(request.form.get("location"))
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm = request.form.get("confirm")
        user_gender = request.form.get("user_gender")
        additional = escape(request.form.get("additional"))
        receive_email = request.form.get("receive_email")
        if not error:
            if first_name:
                user.first_name = first_name
            if birth_date:
                user.birth_date = birth_date
            if email:
                user.email = email
            user.location = location
            user.additional = additional
            if receive_email:
                user.receive_email = True
            else:
                user.receive_email = False
            if old_password and new_password and confirm:
                if new_password == confirm:
                    if bcrypt.checkpw(old_password.encode(), user.password.encode()):
                        user.password = bcrypt.hashpw(
                            new_password.encode(), bcrypt.gensalt()
                        ).decode()
                    else:
                        error = "Old password is incorrect."
                else:
                    error = "Invalid password confirmation."
            if user_gender:
                match user_gender:
                    case "unset":
                        user.user_gender = 1
                    case "woman":
                        user.user_gender = 2
                    case "man":
                        user.user_gender = 4
                    case "beyondbinary":
                        user.user_gender = 8
                    case _:
                        error = "Unknown gender"

            preferred_genders = 0
            if not request.form.get("preference_all"):
                if request.form.get("preference_unset"):
                    preferred_genders += 1
                if request.form.get("preference_woman"):
                    preferred_genders += 2
                if request.form.get("preference_man"):
                    preferred_genders += 4
                if request.form.get("preference_beyondbinary"):
                    preferred_genders += 8
            else:
                preferred_genders = 15
            user.preferred_genders = preferred_genders

            passions = 0
            if request.form.get("passion_traveling"):
                passions += 1
            if request.form.get("passion_reading"):
                passions += 2
            if request.form.get("passion_cooking"):
                passions += 4
            if request.form.get("passion_sports"):
                passions += 8
            if request.form.get("passion_dancing"):
                passions += 16
            if request.form.get("passion_music"):
                passions += 32
            user.passions = passions
            db.session.commit()

            if "avatar" in request.files:
                file = request.files["avatar"]
                if file.filename:
                    file.save(
                        os.path.join(
                            "app",
                            "static",
                            "avatars",
                            str(flask_login.current_user.id) + ".jpg",
                        )
                    )

        if not error:
            return redirect("/dating", code=302)

    return render_template(
        "settings.html",
        error=error,
        first_name=user.first_name,
        birth_date=user.birth_date,
        email=user.email,
        location=user.location,
        user_gender=user.user_gender,
        preference_unset=user.preferred_genders & 1,
        preference_woman=user.preferred_genders & 2,
        preference_man=user.preferred_genders & 4,
        preference_beyondbinary=user.preferred_genders & 8,
        passion_traveling=user.passions & 1,
        passion_reading=user.passions & 2,
        passion_cooking=user.passions & 4,
        passion_sports=user.passions & 8,
        passion_dancing=user.passions & 16,
        passion_music=user.passions & 32,
        additional=user.additional,
        receive_email=user.receive_email,
    )
