from django.contrib import admin
from .models import Conversation, Message, PushSubscription


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'topic', 'is_closed', 'updated_at')
    list_filter = ('topic', 'is_closed')
    search_fields = ('customer__username', 'customer__email')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'sender_is_staff', 'is_read', 'created_at')
    list_filter = ('sender_is_staff', 'is_read')


@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_agent', 'created_at')
    search_fields = ('user__username', 'user__email')
