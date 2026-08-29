def unread_counts(request):
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {}

    if user.is_staff:
        from .models import Conversation
        total = sum(c.unread_for_staff() for c in Conversation.objects.all())
        return {'unread_count': total}

    from .models import Conversation
    conversation = Conversation.objects.filter(customer=user).first()
    if conversation is None:
        return {'unread_count': 0}
    return {'unread_count': conversation.unread_for_customer()}
