from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        ):
            return True


class IsOnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        ):
            return True


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_user
                 or request.user.is_admin
                 or request.user.is_moderator
                 or request.user.is_superuser)
        ):
            return True
