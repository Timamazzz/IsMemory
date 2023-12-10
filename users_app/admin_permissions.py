from rest_framework import permissions


class HasDashboardAdminGroupPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='dahsboard-admin').exists()
