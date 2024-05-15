from rest_framework import permissions


class IsAdminRedact(permissions.BasePermission):

    def has_permission(self, request, view):
        print('IsAdminRedact')
        print('request.user.groups', request.user.groups)
        return request.user.groups.filter(name='dashboard-admin-redact').exists()


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        print('IsAdmin')
        print('request.user.groups', request.user.groups)
        return request.user.groups.filter(name='dashboard-admin').exists()
