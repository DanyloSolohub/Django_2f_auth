from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.api.v1.serializers.users import UserSerializer
from apps.core.models import User


class EmailActiveView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        token = self.request.query_params.get('token')
        try:
            token = AccessToken(token)
            user_id = token.payload.get('user_id')
        except TokenError as err:
            raise ValidationError({'error': str(err)})
        user = get_object_or_404(User, pk=user_id)
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
