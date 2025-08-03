from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class SignalNotificationTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="alice", password="pass")
        self.receiver = User.objects.create_user(
            username="bob", password="pass")

    def test_notification_created_on_message(self):
        self.assertEqual(Notification.objects.count(), 0)
        msg = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Hello Bob")
        # After creation, notification should exist
        notifications = Notification.objects.filter(
            user=self.receiver, message=msg)
        self.assertEqual(notifications.count(), 1)
        notif = notifications.first()
        self.assertFalse(notif.read)
        self.assertIn("New message from", notif.summary)
