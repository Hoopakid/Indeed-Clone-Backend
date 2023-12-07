from rest_framework import permissions


class IsAdminOrParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user in obj.participants.all()
