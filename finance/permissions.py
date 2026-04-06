from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'


class IsAnalystOrAdminReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Safe methods: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return request.user.role in ['Analyst', 'Admin']

        
        return request.user.role == 'Admin'