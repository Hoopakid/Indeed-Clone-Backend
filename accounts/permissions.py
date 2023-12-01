from rest_framework import permissions


class IsSuperUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_superuser and request.user.is_authenticated
        )