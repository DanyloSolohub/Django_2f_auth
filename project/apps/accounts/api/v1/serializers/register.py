from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from apps.accounts.services.auth_ import AuthServices
from apps.core.models import User


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = AuthServices.create_email_token(user)
        data = {
            'subject': 'Activate account',
            'body': f'<b>http://localhost:8000/api/v1/accounts/activate?token={token}<b>',
            'to': [user.email]
        }
        AuthServices.send_mail(**data)
        return user
