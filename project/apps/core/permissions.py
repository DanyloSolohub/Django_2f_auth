from rest_framework.permissions import BasePermission


class Is2FVerified(BasePermission):
    message = 'Two-factor authorization is not passed'

    def has_permission(self, request, view):
        if request.user.is_authenticated and any(devices.confirmed for devices in request.user.totpdevice_set.all()):
            return True
        return False
