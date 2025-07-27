from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        )
        read_only_fields = ('user_id', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Includes nested sender details.
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = (
            'message_id',
            'sender',
            'sender_id',
            'conversation',
            'message_body',
            'sent_at',
        )
        read_only_fields = ('message_id', 'sent_at')

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        validated_data['sender_id'] = sender_id
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Handles many-to-many participants and nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'participants',
            'participant_ids',
            'created_at',
            'messages',
            'message_count',
        )
        read_only_fields = ('conversation_id', 'created_at', 'message_count')

    def validate_participant_ids(self, value):
        if not isinstance(value, list) or len(value) < 2:
            raise serializers.ValidationError(
                'A conversation requires at least two participants.')
        return value

    def get_message_count(self, obj):
        return obj.messages.count()

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participant_ids)
        return conversation
