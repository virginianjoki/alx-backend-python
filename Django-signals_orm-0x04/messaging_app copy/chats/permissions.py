from rest_framework import permissions
from .models import Conversation


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a message to view it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows only participants of a conversation to interact with its messages (view, create, update, delete).
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Support both Message and Conversation objects
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
        else:
            conversation = obj  # obj might be a Conversation

        # Only participants can perform any action (view, update, delete)
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in conversation.participants.all()

        return False
