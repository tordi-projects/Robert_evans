import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages as flash
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Conversation, Message, PushSubscription
from .forms import NewConversationForm, ReplyForm
from .push import notify_user

staff_required = user_passes_test(lambda u: u.is_active and u.is_staff)


@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('messaging:admin_dashboard')
    return redirect('messaging:customer_dashboard')


def _notify_staff(sender, msg):
    """Ping every staff ('Robert') account when a customer messages in."""
    name = sender.get_full_name() or sender.username
    preview = msg.body if len(msg.body) <= 120 else msg.body[:117] + '…'
    for staff_user in get_user_model().objects.filter(is_staff=True, is_active=True):
        notify_user(
            staff_user,
            title=f'New message from {name}',
            body=preview,
            url=f'/inbox/admin/{msg.conversation_id}/',
        )


@login_required
def customer_dashboard(request):
    """A customer's single thread with Robert — send + read replies here."""
    if request.user.is_staff:
        return redirect('messaging:admin_dashboard')

    conversation = Conversation.objects.filter(customer=request.user).first()

    if request.method == 'POST':
        if conversation is None:
            form = NewConversationForm(request.POST)
            if form.is_valid():
                conversation = Conversation.objects.create(
                    customer=request.user, topic=form.cleaned_data['topic']
                )
                msg = Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    body=form.cleaned_data['body'],
                )
                _notify_staff(request.user, msg)
                flash.success(request, "Sent — Robert typically replies within a few hours.")
                return redirect('messaging:customer_dashboard')
        else:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                msg = Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    body=reply_form.cleaned_data['body'],
                )
                _notify_staff(request.user, msg)
                return redirect('messaging:customer_dashboard')

    new_form = NewConversationForm()
    reply_form = ReplyForm()
    thread = []
    if conversation is not None:
        thread = conversation.messages.select_related('sender').all()
        conversation.messages.filter(sender_is_staff=True, is_read=False).update(is_read=True)

    return render(request, 'messaging/customer_dashboard.html', {
        'conversation': conversation,
        'thread': thread,
        'new_form': new_form,
        'reply_form': reply_form,
    })


@staff_required
def admin_dashboard(request):
    """Robert's inbox: every customer conversation, newest activity first."""
    conversations = Conversation.objects.select_related('customer').prefetch_related('messages')
    q = request.GET.get('q', '').strip()
    if q:
        conversations = conversations.filter(
            Q(customer__username__icontains=q) |
            Q(customer__first_name__icontains=q) |
            Q(customer__email__icontains=q)
        )
    conversations = conversations.distinct()

    total_unread = sum(c.unread_for_staff() for c in conversations)

    return render(request, 'messaging/admin_dashboard.html', {
        'conversations': conversations,
        'q': q,
        'total_unread': total_unread,
    })


@staff_required
def admin_conversation(request, pk):
    conversation = get_object_or_404(Conversation.objects.select_related('customer'), pk=pk)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                body=form.cleaned_data['body'],
            )
            preview = form.cleaned_data['body']
            if len(preview) > 120:
                preview = preview[:117] + '…'
            notify_user(
                conversation.customer,
                title=settings.BUSINESS['name'],
                body=preview,
                url='/inbox/dashboard/',
            )
            return redirect('messaging:admin_conversation', pk=pk)
    else:
        form = ReplyForm()

    thread = conversation.messages.select_related('sender').all()
    conversation.messages.filter(sender_is_staff=False, is_read=False).update(is_read=True)

    return render(request, 'messaging/admin_conversation.html', {
        'conversation': conversation,
        'thread': thread,
        'form': form,
    })


@login_required
@require_POST
def push_subscribe(request):
    """Called from the browser once a device is granted notification
    permission and has a Push subscription — stores it against the logged-in
    user so future messages can wake that device."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'ok': False, 'error': 'bad payload'}, status=400)

    endpoint = data.get('endpoint')
    keys = data.get('keys') or {}
    p256dh = keys.get('p256dh')
    auth = keys.get('auth')
    if not (endpoint and p256dh and auth):
        return JsonResponse({'ok': False, 'error': 'missing fields'}, status=400)

    PushSubscription.objects.update_or_create(
        endpoint=endpoint,
        defaults={
            'user': request.user,
            'p256dh': p256dh,
            'auth': auth,
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:255],
        },
    )
    return JsonResponse({'ok': True})


@login_required
@require_POST
def push_unsubscribe(request):
    try:
        data = json.loads(request.body or '{}')
    except (json.JSONDecodeError, TypeError):
        data = {}
    endpoint = data.get('endpoint')
    if endpoint:
        PushSubscription.objects.filter(endpoint=endpoint, user=request.user).delete()
    return JsonResponse({'ok': True})
