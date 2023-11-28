import logging
import smtplib
import os
from dotenv import load_dotenv
load_dotenv("config_file.env")


def send_email( subject, body):
    SUBJECT = subject
    TEXT = body
    message = """From: {}\nSubject: {}\n\n{} """.format(
        os.getenv('FROM_EMAIL'), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT'))
        server.ehlo()
        server.starttls()
        server.login(os.getenv('FROM_EMAIL'), os.getenv('FROM_PWD'))
        server.sendmail(os.getenv('FROM_EMAIL'), os.getenv('FROM_EMAIL'), message)
        server.close()
    except Exception:
        logging.exception('Failed to send email')

