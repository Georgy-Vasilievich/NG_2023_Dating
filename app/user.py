"""User-related functions"""

from datetime import date
from sqlalchemy import func

from app import db
from app.models import User


def calculate_age(birth_date):
    """Calculates user's age"""
    current_date = date.today()
    age = current_date.year - birth_date.year - 1
    if current_date.month > birth_date.month or (
        current_date.month == birth_date.month and current_date.day > birth_date.day
    ):
        age += 1
    return age


def get_gender(gender):
    """Returns gender string based on integer"""
    match gender:
        case 1:
            return "Not set"
        case 2:
            return "Woman"
        case 4:
            return "Man"
        case 8:
            return "Beyond Binary"


def get_passions(passions):
    """Returns passion list string based on integer"""
    passion_list = []
    if passions & 1:
        passion_list.append("Traveling")
    if passions & 2:
        passion_list.append("Reading")
    if passions & 4:
        passion_list.append("Cooking & Baking")
    if passions & 8:
        passion_list.append("Sports & Fitness")
    if passions & 16:
        passion_list.append("Dancing")
    if passions & 32:
        passion_list.append("Music")

    return ", ".join(passion_list) if passions else None


def get_people(user_id):
    """Returns five random matching people for a specified user ID"""
    user = db.session.query(User).get(user_id)
    return (
        User.query.filter(
            User.passions.op("&")(user.passions),
            User.user_gender.op("&")(user.preferred_genders),  # our preference
            User.preferred_genders.op("&")(user.user_gender),  # their preference
            User.id != user.id,
        )
        .order_by(func.random())
        .limit(5)
        .all()
    )
