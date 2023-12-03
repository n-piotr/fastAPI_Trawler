import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.celery import celery, settings


@celery.task()
def send_email(email: str, url: str):

    msg = MIMEMultipart()
    msg['From'] = settings.YANDEX_USER
    msg['To'] = email
    msg['Subject'] = "Email Verify"

    msg.attach(MIMEText(url))

    server = smtplib.SMTP(settings.YANDEX_HOST, settings.YANDEX_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(settings.YANDEX_USER, settings.YANDEX_APP_PASSWORD.get_secret_value())
    server.sendmail(
        settings.YANDEX_USER,
        email,
        msg.as_string()
    )
    server.quit()


# @celery.task()  # ///// Celery test /////
# def ping():
#     print("ECHO from Celery task")
#
#
# @celery.task()  # ///// Celery test crontab-schedules /////
# def beat_ping():
#     print("ECHO-2 from Celery Beat task")
