import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PORT = 587
SMTP_SERVER = 'smtp.gmail.com'
SENDER_EMAIL = 'faculty.electiv.courses@gmail.com'
SENDER_PASSWORD = 'vfsizenwkhheavyw'


def send_email(subject: str, body: str, to: str) -> None:
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to
    msg.attach(MIMEText(body, 'plain'))

    print("Sending email")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print(f"To: {to}")

    try:
        srv = smtplib.SMTP(SMTP_SERVER, PORT)
        srv.starttls()
        srv.login(SENDER_EMAIL, SENDER_PASSWORD)
        srv.send_message(msg)
        srv.quit()

    except Exception as e:
        print(f"Error sending email: {str(e)}")
