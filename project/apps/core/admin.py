from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

from apps.core.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Token'), {'fields': ('token',)}),
    )
    readonly_fields = ('token',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

    def token(self, instance):
        try:
            token = Token.objects.get(user_id=instance.pk)
            return token.key
        except Token.DoesNotExist:
            return None


admin.site.register(User, CustomUserAdmin)
