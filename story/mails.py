import sendgrid
import os
from sendgrid.helpers.mail import *

# this file includes mail functions to send confirm and reset keys to users
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID_API_KEY"))

confirmation_sender = "confirmation@weirdbutreal.com"
confirmation_subject = ", Confirm your mail address to continue having fun with weirdbutreal.com"
confirmation_content = """
This e-mail is sent by www.weirdbutreal.com to confirm your mail address.
You need to click the link below to confirm your credentials and have fun!

"""
def sendconfirmation(owner, to_email, infos, from_email=confirmation_sender, subject=confirmation_subject, content=confirmation_content):
    # Sending confirmation mail
    from_email = Email(from_email)
    to_email = Email(to_email)
    subject = owner + subject
    content = Content("text/plain", content + infos)
    mail = Mail(from_email, subject, to_email, content)
    return sg.client.mail.send.post(request_body=mail.get())


reset_sender = "passwordreset@weirdbutreal.com"
reset_subject = ", forgot your password? Here is the link for resetting your password credentials..."
reset_content = """
This e-mail is sent by www.weirdbutreal.com to reset your password.
If you don't remember your password, click the link below to reset it.

"""
def sendpasswordreset(owner, to_email, infos, from_email=reset_sender, subject=reset_subject, content=reset_content):
    # Sending password reset mail
    from_email =Email(from_email)
    to_email = Email(to_email)
    subject = owner + subject
    content = Content("text/plain", content + infos)
    mail = Mail(from_email, subject, to_email, content)
    return sg.client.mail.send.post(request_body=mail.get())
