from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect('messaging:dashboard_redirect')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name or user.username} — you're all set.")
            return redirect('messaging:dashboard_redirect')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
