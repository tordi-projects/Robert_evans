from django.conf import settings
from django.db import models

TOPIC_CHOICES = [
    ('leak', 'Leak / burst pipe'),
    ('clog', 'Drain or sewer clog'),
    ('install', 'New installation'),
    ('electrical', 'Electrical issue'),
    ('quote', 'Quote request'),
    ('other', 'Something else'),
]


class Conversation(models.Model):
    """A single ongoing thread between one customer and Robert's team."""

    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversation'
    )
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES, default='other')
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'Conversation with {self.customer.get_full_name() or self.customer.username}'

    def unread_for_staff(self):
        return self.messages.filter(is_read=False, sender_is_staff=False).count()

    def unread_for_customer(self):
        return self.messages.filter(is_read=False, sender_is_staff=True).count()

    def last_message(self):
        return self.messages.order_by('-created_at').first()


class PushSubscription(models.Model):
    """One browser/device subscription for a logged-in user. A user can have
    several (phone, laptop, etc.) — we notify all of them."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='push_subscriptions'
    )
    endpoint = models.URLField(max_length=500, unique=True)
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Push subscription for {self.user} ({self.endpoint[:40]}…)'


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    # Denormalised for quick unread queries without joining to the user each time.
    sender_is_staff = models.BooleanField(default=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} @ {self.created_at:%Y-%m-%d %H:%M}'

    def save(self, *args, **kwargs):
        self.sender_is_staff = bool(self.sender.is_staff)
        super().save(*args, **kwargs)
        self.conversation.save(update_fields=['updated_at'])

