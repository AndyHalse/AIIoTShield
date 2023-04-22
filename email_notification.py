import smtplib
from email.message import EmailMessage
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPDataError, SMTPHeloError, SMTPException


def send_email_notification(subject, body):
    """

    :param subject:
    :param body:
    :return:
    """
    sender_email = "sender_andy@acsltd.eu"
    sender_password = "Kubo1966&&"
    recipient_email = "andy@acsltd.eu"

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.ionos.co.uk", 587) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            return True
    except (SMTPAuthenticationError, SMTPConnectError, SMTPDataError, SMTPHeloError, SMTPException) as e:
        print(f"Error sending email: {e}")
        return False

# Example usage:
# send_email_notification("Subject", "Body", "sender_email", "sender_password", "recipient_email")
