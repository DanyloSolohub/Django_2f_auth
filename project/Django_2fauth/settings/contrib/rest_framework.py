REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'Django_2fauth.settings.contrib.expire_token.ExpiringTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
