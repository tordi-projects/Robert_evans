from django.conf import settings


def business_info(request):
    """Makes BUSINESS dict + the public VAPID key available in every
    template, so base.html can hand the key to push.js without a view."""
    return {
        'business': settings.BUSINESS,
        'vapid_public_key': settings.VAPID_PUBLIC_KEY,
    }
