from rest_framework import permissions

from main.models import JobCreate


class CanCreateJobPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                job_create_status = request.user.jobcreate.status
                return job_create_status == 1
            except JobCreate.DoesNotExist:
                return False
        return False


class IsHisObjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
