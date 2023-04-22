import smtplib
from email.message import EmailMessage


def send_email(subject, body, to_email, from_email, password):
    """

    :param subject:
    :param body:
    :param to_email:
    :param from_email:
    :param password:
    """
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()
