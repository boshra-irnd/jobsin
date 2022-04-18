from rest_framework import permissions
from .models import Employee

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    

class IsOwnUserOrReadOnly(permissions.BasePermission):
    message = 'Editing detail is rstricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj.user == request.user and obj.user.role == 'E')
    
class IsOwnUserOrReadOnly2(permissions.BasePermission):
    message = 'Editing detail is rstricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj.employee.user == request.user)
    
class IsOwnUserOrReadOnly3(permissions.BasePermission):
    message = 'Editing detail is rstricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj.employee.user == request.user)