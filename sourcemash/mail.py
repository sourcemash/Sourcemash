from flask_mail import Mail

mail = Mail()


def send_security_email(msg):
    mail.send(msg)
