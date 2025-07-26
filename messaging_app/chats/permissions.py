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
    Custom permission to allow only authenticated users who are participants of a conversation
    to view, send, update or delete messages.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be a Message or Conversation depending on the view.
        We assume the Message model has a `conversation` ForeignKey.
        """
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
        else:
            conversation = obj  # If the object itself is a conversation

        return request.user in conversation.participants.all()
