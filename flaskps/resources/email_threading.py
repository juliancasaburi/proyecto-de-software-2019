import threading
from flask import copy_current_request_context, current_app as app
from flask_mail import Mail, Message


def create_message(recipient, subject, html):
    if not recipient:
        raise ValueError("Target email not defined.")

    return Message(
        subject,
        [recipient],
        html=html,
        sender=app.config["MAIL_USERNAME"],
        charset="utf8",
    )


def send_async(recipient, subject, html):
    message = create_message(recipient, subject, html)

    @copy_current_request_context
    def send_message(message):
        mail = Mail(app)
        mail.send(message)

    sender = threading.Thread(name="mail_sender", target=send_message, args=(message,))
    sender.start()
