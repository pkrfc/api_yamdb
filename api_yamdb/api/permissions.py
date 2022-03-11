from rest_framework import permissions


class IsOnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ReviewCommentPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator)


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )
