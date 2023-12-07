from rest_framework import permissions

from main.models import JobCreate


class CanCreateJobPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                job_create_instance = request.user.jobcreate_set.first()
                return job_create_instance is not None and job_create_instance.status == JobCreate.YES
            except JobCreate.DoesNotExist:
                return False
        return False


class IsHisObjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
