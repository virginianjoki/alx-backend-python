from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if not created:
        return  # only on first creation

    # Avoid duplicate notifications in weird edge cases
    Notification.objects.create(
        user=instance.receiver,
        message=instance,
        summary=f"New message from {instance.sender.username}"
    )
