from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    message = "You do not have permission to access this note."

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin_user():
            return True
        return obj.owner == request.user