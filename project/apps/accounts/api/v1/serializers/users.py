from django.contrib.auth.models import Permission
from rest_framework import serializers, exceptions

from apps.core.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    all_permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser')
        read_only_fields = ('last_login', 'date_joined')

    def get_all_permissions(self, instance: User):
        if instance.is_superuser:
            return Permission.objects.values_list('pk', flat=True)
        return instance.get_all_permissions()

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        permissions = validated_data.pop('user_permissions', [])
        user = User.objects.create_user(**validated_data)
        user.groups.set(groups)
        user.user_permissions.set(permissions)
        return user

    def update(self, instance: User, validated_data):
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', [])
        permissions = validated_data.pop('user_permissions', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if groups:
            instance.groups.set(groups)
        if permissions:
            instance.user_permissions.set(permissions)
        return instance
