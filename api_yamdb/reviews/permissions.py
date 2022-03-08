from rest_framework import permissions


class ReviewPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.method in permissions.SAFE_METHODS \
            or obj.author == request.user \
                and request.user.is_moderator
