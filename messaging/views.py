from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages as flash
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Conversation, Message
from .forms import NewConversationForm, ReplyForm

staff_required = user_passes_test(lambda u: u.is_active and u.is_staff)


@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('messaging:admin_dashboard')
    return redirect('messaging:customer_dashboard')


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
                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    body=form.cleaned_data['body'],
                )
                flash.success(request, "Sent — Robert typically replies within a few hours.")
                return redirect('messaging:customer_dashboard')
        else:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    body=reply_form.cleaned_data['body'],
                )
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
