import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages by conversation with a specific user
    user = django_filters.NumberFilter(field_name='conversation__participants__id')
    # Filter messages sent after a certain datetime
    sent_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    # Filter messages sent before a certain datetime
    sent_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['user', 'sent_after', 'sent_before']