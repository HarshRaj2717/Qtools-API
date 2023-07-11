from django.shortcuts import render
from django.http import HttpResponse
from . import users_helper
from . import models

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register_user(request, **kwargs):
    ...


def login_user(request):
    ...


def update_user(request):
    ...


def forgot_password(request):
    ...
