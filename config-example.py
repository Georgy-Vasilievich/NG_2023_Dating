"""
Database configuration file. Should be renamed to config.py
"""


import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "change this"

mail_server = "mail.example.com"
mail_user = "user@example.com"
mail_email = "user@example.com"
mail_password = "example"
mail_port = 587
mail_security = "starttls" # "none"/"starttls"/"tls"

send_emails = True
