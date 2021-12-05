import pyqrcode
import base64
import io

from django.utils import timezone
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status, views
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    """

    def post(self, request):
        user = request.user
        device = get_user_totp_device(user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        url_qr = pyqrcode.create(url)
        file_obj = io.BytesIO()
        url_qr.png(file_obj, scale=8)
        encoded = base64.b64encode(file_obj.getvalue()).decode('ascii')
        return Response({'qr_code': encoded}, status=status.HTTP_201_CREATED)


class TOTPVerifyView(views.APIView):
    """
    Use this endpoint to login with TOTP device
    """

    def post(self, request, auth_key):
        user = request.user
        device = get_user_totp_device(user)
        if not (device and device.verify_token(auth_key)):
            raise ValidationError({'error': 'Invalid auth key'})
        device.confirmed = True
        device.save()
        user.is_new_user = False
        user.last_login = timezone.now()
        user.save()
        user_token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': user_token.key,
                         'user_id': user.id,
                         'first_name': user.first_name,
                         'last_name': user.last_name,
                         'email': user.email}, status=status.HTTP_200_OK)
