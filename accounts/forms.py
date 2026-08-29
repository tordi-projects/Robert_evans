from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label='Full name')
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=30, required=False, label='Phone (optional)')
    address = forms.CharField(max_length=255, required=False, label='Address (optional)')

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username']

    field_order = ['first_name', 'email', 'phone', 'address', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone', '')
            profile.address = self.cleaned_data.get('address', '')
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']
