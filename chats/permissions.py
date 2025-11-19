from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user


class IsMessageOwner(permissions.BasePermission):
    """
    Permission to only allow owners of a message to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user


class IsConversationParticipant(permissions.BasePermission):
    """
    Permission to only allow participants of a conversation to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsUserProfileOwner(permissions.BasePermission):
    """
    Permission to only allow user to access their own profile.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user