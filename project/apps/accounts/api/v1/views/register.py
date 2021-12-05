from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from apps.accounts.api.v1.serializers.register import UserRegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
