from datetime import timedelta

from django.core import mail
from rest_framework_simplejwt.tokens import RefreshToken


class EmailToken(RefreshToken):
    lifetime = timedelta(days=1)


class AuthServices:
    @staticmethod
    def send_mail(subject, body, to, **kwargs):
        message = mail.EmailMessage(subject, body, to=to, **kwargs)
        message.content_subtype = "html"
        message.send()

    @staticmethod
    def create_email_token(user):
        return EmailToken().for_user(user).access_token
