
from rest_framework import permissions
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Check if the authenticated user is the author 
    if yes then permit it to perform CRUD else let them just view
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated is True
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user  
    