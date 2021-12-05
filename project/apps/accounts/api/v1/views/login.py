from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import exceptions, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema

from apps.accounts.api.v1.serializers.register import UserRegisterSerializer


class UserLoginView(GenericAPIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request, *args, **kwargs):
        username = request.data.get('email')
        password = request.data.get('password')
        if not (username or password):
            raise exceptions.ValidationError('Please provide both username and password')
        user = authenticate(username=username, password=password)
        if not user:
            raise exceptions.NotFound('Invalid Credentials')
        token, _ = Token.objects.update_or_create(user=user,
                                                  defaults={'created': timezone.now(),
                                                            })
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
