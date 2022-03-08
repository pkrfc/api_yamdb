from rest_framework import permissions


<<<<<<< HEAD
class IsAdminOrReadOnly(permissions.BasePermission):
=======
class OwnerOrReadOnly(permissions.BasePermission):
>>>>>>> origin/develop_2

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
<<<<<<< HEAD
            and (request.user.is_admin
                 or request.user.is_superuser)
        )


class IsOnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        )


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
=======
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AdminOrReadOnly(permissions.BasePermission):
>>>>>>> origin/develop_2

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
<<<<<<< HEAD
            or request.user.is_authenticated
            and (request.user.is_user
                 or request.user.is_admin
                 or request.user.is_moderator
                 or request.user.is_superuser)
=======
            or permissions.IsAdminUser()
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or permissions.IsAdminUser()
>>>>>>> origin/develop_2
        )
