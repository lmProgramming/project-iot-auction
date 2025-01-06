from django.shortcuts import render
from django.db.models.manager import BaseManager
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request) -> HttpResponse:
    return render(request, 'index.html')
