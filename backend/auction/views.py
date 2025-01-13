from django.shortcuts import render
from django.db.models.manager import BaseManager
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from auction.forms import ArticleForm, RegistrationForm
from .models import Auction, Article, User, Wallet
from .serializers import AuctionSerializer, ItemSerializer, UserSerializer


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

    def perform_create(self, serializer):
        serializer.save()
        # Notify Raspberry Pis via MQTT
        import paho.mqtt.client as mqtt

        client = mqtt.Client()
        client.connect("localhost", 1883, 60)
        client.publish(f"auction/{serializer.instance.id}", "start")
        client.disconnect()



def create_article(request, card_id: int):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ArticleForm()
    return render(request, "create_article.html", {"form": form})


def register(request, card_id: int):
    try:
        wallet = Wallet.objects.filter(card_id=card_id)
        if wallet:
            return HttpResponse("User already registered")
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(card_id=card_id, balance=0.0)

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
                age=form.cleaned_data["age"],
                wallet=wallet,
            )

            return redirect("/")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form, "card_id": card_id})


# Create your views here.


def index(request) -> HttpResponse:
    return render(request, "index.html")
