from rest_framework import permissions


class IsAdminRedact(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='dahsboard-admin-redact').exists()


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='dahsboard-admin').exists()
