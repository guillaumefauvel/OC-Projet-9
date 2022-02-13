from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login

from . import forms


def signup_page(request):
    """ Create an account in order to login """

    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})
