import smtplib
from email.message import EmailMessage
from os import environ

def sendEmail(subject, body, to):

    # create EmailMessage object
    message = EmailMessage()
    # set the body of mail
    message.set_content(body)
    message['subject'] = subject
    message['to'] = to

    sender = environ["SYSTEM_EMAIL"]
    password = environ["SYSTEM_EMAIL_PASSKEY"]

    message['from'] = sender
    try:

        server = smtplib.SMTP(environ["SYSTEM_EMAIL_HOST"], environ["SYSTREM_EMAIL_PORT"])
        server.starttls()
        server.login(sender, password)
        # send mail
        server.send_message(message)

        server.quit()

    except:

        server.quit()
