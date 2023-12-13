"""This file contain the rules page"""

from flask import Blueprint

from app import app

rules_bp = Blueprint("rules", __name__)


@app.route("/rules", methods=["GET"])
def rules():
    return app.send_static_file("rules.html")
