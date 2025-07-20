from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.

    Endpoints:
        GET    /conversations/         -> list all conversations
        POST   /conversations/         -> create a new conversation
        GET    /conversations/{id}/    -> retrieve a specific conversation
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and sending messages.

    Endpoints:
        GET    /messages/              -> list all messages
        POST   /messages/              -> send a new message to a conversation
        GET    /messages/{id}/         -> retrieve a specific message
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Associates the message sender to the authenticated user if not provided
        if 'sender_id' not in serializer.validated_data:
            serializer.save(sender=self.request.user)
        else:
            serializer.save()
