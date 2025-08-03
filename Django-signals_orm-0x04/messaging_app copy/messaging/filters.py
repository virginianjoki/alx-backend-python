import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    sent_before = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte")
    sent_after = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte")
    sender_email = django_filters.CharFilter(
        field_name="sender__email", lookup_expr="icontains")

    class Meta:
        model = Message
        fields = ['conversation', 'sender_email', 'sent_before', 'sent_after']
