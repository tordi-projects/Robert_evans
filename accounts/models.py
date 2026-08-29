from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extra contact details for a customer account, kept separate from
    Django's built-in User model so authentication stays standard."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profile<{self.user.username}>'
