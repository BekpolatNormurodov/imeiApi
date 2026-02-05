from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsJtonOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.jton == request.user.jton


class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
