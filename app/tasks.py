import logging
from typing import List

from celery import current_app as celery
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config


@celery.task
def send_email_task(subject: str, recipients: List[str], body: str, sender=None) -> None:
    if not sender:
        sender = Config.DEFAULT_SENDER

    if not recipients:
        raise ValueError("No recipients provided")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            smtp.sendmail(sender, recipients, msg.as_string())
    except Exception as e:
        logging.warning(e)
