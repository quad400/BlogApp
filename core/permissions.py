from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        Permissions to allow only the owner to modify the instance
        and allow others to only view it
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.post_user == request.user