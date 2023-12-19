"""This file contains the logout function"""

from flask import Blueprint, redirect
import flask_login

from app import app

logout_bp = Blueprint("logout", __name__)


@app.route("/logout", methods=["GET"])
def logout():
    flask_login.logout_user()
    return redirect("/", code=302)
