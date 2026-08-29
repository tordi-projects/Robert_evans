from django import forms
from .models import Conversation, TOPIC_CHOICES


class NewConversationForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES, label='What do you need help with?')
    body = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': "Describe the issue — location in the house, how urgent it is, anything you've already tried."}),
        label='Message',
    )


class ReplyForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a reply…'}),
        label='',
    )
