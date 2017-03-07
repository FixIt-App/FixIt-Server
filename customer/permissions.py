from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to get, edit, delete.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        if(hasattr(obj, 'user')):
            return obj.user == request.user
        elif (hasattr(obj, 'customer')):
            return obj.customer.user == request.user
        else:
            return False