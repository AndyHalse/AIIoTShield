import os
import smtplib
import ssl
from email.message import EmailMessage

class EmailNotification:
    def __init__(self, sender_email, sender_password, recipient_email, smtp_host, smtp_port):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send_notification(self, subject, body):
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_email

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                print("Email sent successfully")
                return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"Error authenticating: {e}")
        except (smtplib.SMTPConnectError, smtplib.SMTPDataError, smtplib.SMTPHeloError) as e:
            print(f"Error connecting to SMTP server: {e}")
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")
        return False
        
if __name__ == '__main__':
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.ionos.co.uk')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'sender@example.com')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'password')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'recipient@example.com')
    
    email_notification = EmailNotification(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, SMTP_HOST, SMTP_PORT)
    success = email_notification.send_notification("Test Subject", "This is a test email from EmailNotification class")
    if success:
        print("Test email sent successfully")
    else:
        print("Failed to send test email")
