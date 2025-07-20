from django.db import models

# Create your models here.
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Attributes:
        id (UUID): Primary key for the user.
        email (str): Unique email address for the user.
        phone_number (str): Optional contact number.
        role (str): User role - guest, host, or admin.
        created_at (datetime): Timestamp when the user was created.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        null=False,
        default='guest'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"


class Conversation(models.Model):
    """
    Model representing a conversation between users.

    Attributes:
        id (UUID): Primary key for the conversation.
        participants (ManyToMany): Users involved in the conversation.
        created_at (datetime): Timestamp when conversation was created.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        users = ", ".join([u.email for u in self.participants.all()])
        return f"Conversation {self.id} between: {users}"


class Message(models.Model):
    """
    Model representing a message sent by a user within a conversation.

    Attributes:
        id (UUID): Primary key for the message.
        sender (ForeignKey): The user who sent the message.
        conversation (ForeignKey): The conversation the message belongs to.
        body (str): The text content of the message.
        sent_at (datetime): Timestamp when the message was sent.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.email} at {self.sent_at}"
