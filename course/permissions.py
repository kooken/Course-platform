from rest_framework.permissions import BasePermission


class Staff(BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(name="moderators").exists()


class Owner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
