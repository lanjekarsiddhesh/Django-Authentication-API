from django.core.mail import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['mail_subject'], 
            body=data['mail_body'], 
            from_email= os.getenv('EMAIL_FROM'),
            to=[data['to']]
            ) #to is a list of email addresses
        email.send()

