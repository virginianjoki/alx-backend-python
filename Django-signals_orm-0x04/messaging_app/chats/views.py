from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from .permissions import IsMessageOwner
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter


class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwner]


class YourMessageView(APIView):
    permission_classes = [IsAuthenticated]
    ...


# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated, IsParticipantOfConversation]

#     filter_backends = [
#         filters.SearchFilter,
#         filters.OrderingFilter,
#         DjangoFilterBackend  # <-- important!
#     ]

#     filterset_class = MessageFilter
#     search_fields = ['body', 'sender__email']
#     ordering_fields = ['sent_at']

#     def get_queryset(self):
#         # Filter only messages from conversations the user is part of
#         return Message.objects.filter(conversation__participants=self.request.user)


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
    ViewSet for listing, retrieving, sending, and managing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['body', 'sender__email']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        # Only return messages in conversations the user is a participant of
        return Message.objects.filter(conversation__participants=self.request.user)

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend  # <-- important!
    ]

    filterset_class = MessageFilter
    search_fields = ['body', 'sender__email']
    ordering_fields = ['sent_at']

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if self.request.user not in conversation.participants.all():
            # If user is not a participant, block message creation
            raise permissions.PermissionDenied(
                "You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = serializer.validated_data.get("conversation").id
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = serializer.save(
            sender=request.user, conversation=conversation)
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
