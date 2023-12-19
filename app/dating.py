"""This file contains the main page"""

from flask import Blueprint, render_template
import flask_login
import os

from app import app
from app.user import calculate_age, get_gender, get_passions, get_people
from app.models import User

dating_bp = Blueprint("dating", __name__)


@app.route("/dating", methods=["GET"])
@flask_login.login_required
def dating():
    people = ""
    users = get_people(flask_login.current_user.id)
    for person in users:
        avatar_exists = os.path.isfile(
            os.path.join("app", "static", "avatars", str(person.id) + ".jpg")
        )
        people += f"""<img src="static/{("avatars/" + str(person.id) + ".jpg") if avatar_exists else "placeholder.png"}" alt="{person.id}'s avatar" width=150>
        <p>
        First name: {person.first_name}<br>
        Age: {calculate_age(person.birth_date)}<br>
        E-mail: <a href="mailto:{person.email}">{person.email}</a><br>
        Location: {person.location}<br>
        Gender: {get_gender(person.user_gender)}<br>
        Passions: {get_passions(person.passions)}<br>
        Additional information: {person.additional}
        </p>
        <hr>\n"""

    return render_template("dating.html", people=people)
