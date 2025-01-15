import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP configuration constants
PORT = 587
SMTP_SERVER = 'smtp.gmail.com'
SENDER_EMAIL = 'faculty.electiv.courses@gmail.com'
SENDER_PASSWORD = 'vfsizenwkhheavyw'

def send_email(subject: str, body: str, to: str) -> None:
    """
    Sends an email using the specified subject, body, and recipient.

    Args:
        subject (str): The subject of the email.
        body (str): The body/content of the email.
        to (str): The recipient's email address.

    Returns:
        None

    This function connects to the SMTP server (Gmail in this case), authenticates with the sender's
    email and password, sends the email, and then terminates the connection.
    If there is an error during the process, it is caught, but not printed.
    """
    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server and send the email
        srv = smtplib.SMTP(SMTP_SERVER, PORT)
        srv.starttls()  # Secure the connection
        srv.login(SENDER_EMAIL, SENDER_PASSWORD)  # Log in with sender's credentials
        srv.send_message(msg)  # Send the email
        srv.quit()  # Terminate the connection

    except Exception as e:
        # Handle exceptions silently (error is not printed)
        pass
