Module src.util.mail_gen
========================

Functions
---------

`send_email(subject: str, body: str, to: str) ‑> None`
:   Sends an email using the specified subject, body, and recipient.
    
    Args:
        subject (str): The subject of the email.
        body (str): The body/content of the email.
        to (str): The recipient's email address.
    
    Returns:
        None
    
    This function connects to the SMTP server (Gmail in this case), authenticates with the sender's
    email and password, sends the email, and then terminates the connection.
    If there is an error during the process, it is caught, but not printed.