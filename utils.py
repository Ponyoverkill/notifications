import smtplib
from email.mime.text import MIMEText

from bson import ObjectId

from config import SMTP_HOST, SMTP_PORT, SMTP_NAME, SMTP_PASSWORD, SMTP_LOGIN, SMTP_EMAIL


def next_oid(oid: ObjectId | str):
    return hex(int(str(oid), 16) + 1)[2:]


async def send_email(email: str, msg: str):
    print('send email')
    mail = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    mail.starttls()
    message = MIMEText(msg)
    message["Subject"] = "notification"
    message["From"] = SMTP_NAME
    message["To"] = email
    mail.login(SMTP_LOGIN, SMTP_PASSWORD)
    mail.sendmail(SMTP_EMAIL, email, message.as_string())
    mail.quit()

