import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def notify_user(user, title, body, url='/'):
    """Push a notification to every device `user` is subscribed on.

    Fails silently (per-subscription) so one dead device never breaks a
    reply — expired subscriptions (404/410 from the push service) are
    cleaned up automatically.
    """
    try:
        from pywebpush import webpush, WebPushException
    except ImportError:
        logger.warning("pywebpush is not installed — run `pip install -r requirements.txt`.")
        return

    subs = list(user.push_subscriptions.all())
    if not subs:
        return

    payload = json.dumps({'title': title, 'body': body, 'url': url})

    for sub in subs:
        try:
            webpush(
                subscription_info={
                    'endpoint': sub.endpoint,
                    'keys': {'p256dh': sub.p256dh, 'auth': sub.auth},
                },
                data=payload,
                vapid_private_key=settings.VAPID_PRIVATE_KEY_PATH,
                vapid_claims={'sub': settings.VAPID_CLAIMS_EMAIL},
            )
        except WebPushException as exc:
            status = getattr(exc.response, 'status_code', None)
            if status in (404, 410):
                sub.delete()  # the browser/OS dropped this subscription — stop trying it
            else:
                logger.warning("Push to %s failed: %s", user, exc)
