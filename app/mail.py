"""E-mail sending code"""

from email.message import EmailMessage
import smtplib
import ssl
import time

from app.models import User
from app.user import calculate_age, get_gender, get_passions, get_people
import config


def send_email(destination, people):
    """Sends an email to a specified destination with a people list"""
    msg = EmailMessage()

    msg["Subject"] = "Dating choices"
    msg["From"] = config.mail_from
    msg["To"] = destination

    text = "Greetings,\n\nAccording to your preferences, we are sending you a daily report about our dating website.\n\n"

    if people:
        text += f"The following people are currently registered on our website that match your settings:\n\n{people}\n\n"
    else:
        text += "There are no people registered on our website that match your preferences.\n\n"

    text += "If you wish to not receive these notifications, disable them in your account settings.\n\nOnlineDating"

    msg.set_content(text)

    password = config.mail_password

    if config.mail_security == "tls":
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            config.mail_server, config.mail_port, context=context
        ) as server:
            server.login(config.mail_user, config.mail_password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(config.mail_server, config.mail_port) as server:
            if config.mail_security == "starttls":
                context = ssl.create_default_context()
                server.starttls(context=context)
            server.login(config.mail_user, config.mail_password)
            server.send_message(msg)


def mail_sender(app_context):
    """Sends e-mail to people who subscribed for them, each 24 hours"""
    while True:
        print("Sending letters to people...")
        with app_context:
            users = User.query.filter(User.receive_email == True).all()
            for user in users:
                people_list = get_people(user.id)
                people = ""
                for person in people_list:
                    people += f"""First name: {person.first_name}
    Age: {calculate_age(person.birth_date)}
    E-mail: {person.email}
    Location: {person.location}
    Gender: {get_gender(person.user_gender)}
    Passions: {get_passions(person.passions)}
    Additional information: {person.additional}
    
    """
                send_email(user.email, people)

        print("Letters sent, waiting 24 hours.")
        time.sleep(86400)
