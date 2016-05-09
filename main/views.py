from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import (HttpResponseForbidden,
                         HttpResponseNotAllowed,
                         HttpResponseBadRequest)
from django.shortcuts import render, redirect

from main.models import Invite


def index_view(request):
    return render(request, 'index.html')


def signin_view(request):
    if request.user.is_authenticated():
        return redirect('inviter:index')
    if request.method == 'GET':
        form = AuthenticationForm(request)
        return render(request, 'signin.html', context=dict(form=form))
    form = AuthenticationForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'signin.html', context=dict(form=form),
                      status=HttpResponseForbidden.status_code)
    user = form.get_user()
    login(request, user)
    return redirect('inviter:index')


def signout_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))
    if request.method == 'POST' and request.user.is_authenticated():
        logout(request)
    return redirect('inviter:index')


def use_invite_view(request, code):
    if request.user.is_authenticated():
        redirect('inviter:index')

    if not code or len(code) != settings.INVITE_CODE_LENGTH \
            or not code.isdigit():
        return render(request,
                      'invalid_code.html',
                      context=dict(code_error='invalid'),
                      status=HttpResponseBadRequest.status_code)
    password = User.objects.make_random_password(
        length=settings.PASSWORD_LENGTH,
        allowed_chars=settings.PASSWORD_CHARS
    )
    try:
        invite = Invite.objects.get(code=code, user=None)
    except Invite.DoesNotExist:
        return render(request,
                      'invalid_code.html',
                      context=dict(code_error='used'),
                      status=HttpResponseBadRequest.status_code)
    invite.user = User.objects.create_user(invite.email, invite.email, password)
    invite.save()
    auth_user = authenticate(username=invite.email, password=password)
    login(request, auth_user)

    settings.MAILER.send('registration_successful', [invite.email],
                         context=dict(
                             password=password,
                             username=invite.email
                         ))
    return redirect('inviter:index')
