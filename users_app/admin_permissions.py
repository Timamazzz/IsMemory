from rest_framework import permissions


class IsAdminRedact(permissions.BasePermission):

    def has_permission(self, request, view):
        print('IsAdminRedact')
        print('request.user', request.user)
        print('request.user.groups', request.user.groups.all())
        print('dashboard-admin-redact', request.user.groups.filter(name='dashboard-admin-redact'))
        print('bool', request.user.groups.filter(name='dashboard-admin-redact').exists())
        return request.user.groups.filter(name='dashboard-admin-redact').exists()


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        print('IsAdmin')
        print('request.user', request.user)
        print('request.user.groups', request.user.groups.all())
        print('dashboard-admin', request.user.groups.filter(name='dashboard-admin'))
        print('bool', request.user.groups.filter(name='dashboard-admin').exists())
        return request.user.groups.filter(name='dashboard-admin').exists()
