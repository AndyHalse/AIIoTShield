import os
import smtplib
import zipfile
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def collect_logs():
    log_files = []
    log_dir = "logs"
    for root, dirs, files in os.walk(log_dir):
        for file in files:
            log_files.append(os.path.join(root, file))
    return log_files

def create_zip(log_files):
    zip_file = "logs.zip"
    with zipfile.ZipFile(zip_file, "w") as z:
        for log_file in log_files:
            z.write(log_file, os.path.basename(log_file))
    return zip_file

def request_approval():
    approval = input("Do you approve sending the logs to AI Cyber Solutions Ltd? (yes/no): ")
    return approval.lower() == "yes"

def send_email(zip_file):
    email = "info@aicybersolutions.eu"
    subject = "IoTShield Bug Report"

    msg = MIMEMultipart()
    msg["From"] = "customer@example.com"  # Replace with customer's email
    msg["To"] = email
    msg["Subject"] = subject

    with open(zip_file, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", f"attachment; filename={zip_file}")
        msg.attach(attachment)

    with smtplib.SMTP_SSL("smtp.example.com", 465) as server:  # Replace with customer's SMTP server and port
        server.login("username", "password")  # Replace with customer's email username and password
        server.send_message(msg)

    print("Logs have been sent successfully.")

def main():
    log_files = collect_logs()
    zip_file = create_zip(log_files)

    if request_approval():
        send_email(zip_file)
    else:
        print("Sending logs has not been approved. The process has been canceled.")

if __name__ == "__main__":
    main()
