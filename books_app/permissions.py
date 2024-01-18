from rest_framework import permissions


class ReadOnlyOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access (GET requests) to all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Restrict write operations to admin users only
        return request.user and request.user.is_staff
