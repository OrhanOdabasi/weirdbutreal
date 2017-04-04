import sendgrid
import os
from sendgrid.helpers.mail import *

# this file includes mail functions to send confirm and reset keys to users
# sendgrid_api = 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
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID_API_KEY"))

confirmation_sender = "confirmation@weirdbutreal.com"
confirmation_subject = "Confirm your mail address to continue having fun with weirdbutreal.com, "
confirmation_content = "This is simple content for confirming your account"
def sendconfirmation(owner, to_email, from_email=confirmation_sender, subject=confirmation_subject, content=confirmation_content):
    # Sending confirmation mail
    from_email = Email(from_email)
    to_email = Email(to_email)
    subject = subject + owner
    content = Content("text/plain", content)
    mail = Mail(from_email, subject, to_email, content)
    return sg.client.mail.send.post(request_body=mail.get())


reset_sender = "passwordreset@weirdbutreal.com"
reset_subject = "Forgot your password? Here is the link for resetting your password credentials..."
reset_content = "this is soimple content for resetting password"
def sendpasswordreset(owner, to_email, from_email=reset_sender, subject=reset_subject, content=reset_content):
    # Sending password reset mail
    from_email =Email(from_email)
    to_mail = Email(to_mail)
    subject = subject + owner
    content = Content("text/plain", content)
    mail = Mail(from_email, subject, to_email, content)
    return sg.client.mail.send.post(request_body=mail.get())
