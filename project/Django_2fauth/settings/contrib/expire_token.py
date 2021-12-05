from datetime import timedelta

from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

TIME_SESSION = timedelta(hours=8)


def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = TIME_SESSION - time_elapsed
    return left_time


def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token, _ = Token.objects.update_or_create(user=token.user)
    return is_expired, token


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise exceptions.AuthenticationFailed('Token has expired')
        return token.user, token
