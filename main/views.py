from django.shortcuts import render


def index_view(request):
    return render(request, 'index.html')


def signup_view(request):
    pass


def signin_view(request):
    pass


def signout_view(request):
    pass


def use_invite_view(request, code):
    pass
