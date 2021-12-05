from django.urls import path, re_path
from apps.accounts.api.v1.views.login import UserLoginView
from apps.accounts.api.v1.views.register import RegisterView
from apps.accounts.api.v1.views.email_activate import EmailActiveView
from apps.accounts.api.v1.views.totp import (TOTPVerifyView, TOTPCreateView)


urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('activate/', EmailActiveView.as_view()),
    path('register/', RegisterView.as_view()),
    path('totp/create/', TOTPCreateView.as_view()),
    re_path(r'^totp/login/(?P<auth_key>[0-9]{6})/$', TOTPVerifyView.as_view())
]
