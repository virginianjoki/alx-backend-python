from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .permissions import IsMessageOwner
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import IsParticipantOfConversation


class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwner]


class YourMessageView(APIView):
    permission_classes = [IsAuthenticated]
    ...


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Filter only messages from conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)


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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email']
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )


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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['body', 'sender__email']
    ordering_fields = ['sent_at']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(sender=request.user)
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
