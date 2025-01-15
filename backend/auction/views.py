from django.shortcuts import render
from django.db.models.manager import BaseManager
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

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


class AuctionListView(ListView):
    model = Auction
    template_name = "auction_list.html"
    context_object_name = "auctions"


class ArticleListView(ListView):
    model = Article
    template_name = "article_list.html"
    context_object_name = "articles"


class UserListView(ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "users"


class WalletListView(ListView):
    model = Wallet
    template_name = "wallet_list.html"
    context_object_name = "wallets"


class AuctionCreateView(CreateView):
    model = Auction
    fields = ["article", "start_time", "end_time", "current_price"]
    template_name = "auction_form.html"
    success_url = reverse_lazy("auction_list")


class ArticleCreateView(CreateView):
    model = Article
    fields = ["name", "owner", "starting_price", "description", "image"]
    template_name = "article_form.html"
    success_url = reverse_lazy("article_list")


class UserCreateView(CreateView):
    model = User
    fields = ["name", "surname", "login", "password", "age", "wallet"]
    template_name = "user_form.html"
    success_url = reverse_lazy("user_list")


class WalletCreateView(CreateView):
    model = Wallet
    fields = ["card_id", "balance"]
    template_name = "wallet_form.html"
    success_url = reverse_lazy("wallet_list")


def register(request, card_id: int):
    wallet = None
    wallet_qs = Wallet.objects.filter(card_id=card_id)

    # Create wallet if it doesn't exist
    if wallet_qs.exists():
        wallet = wallet_qs.first()
        return redirect("/")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            wallet = Wallet.objects.create(card_id=card_id, balance=2500)
            user = User.objects.create(
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
                age=form.cleaned_data["age"],
                login=form.cleaned_data["login"],
                password=form.cleaned_data["password"],
                wallet=wallet,
            )
            print(user)
            return redirect("/")
        else:
            print(form.errors)
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form, "card_id": card_id})


def check_registered(request, card_id: int):
    try:
        wallet_qs = Wallet.objects.filter(card_id=card_id)
        if wallet_qs.exists():
            user = User.objects.get(wallet=wallet_qs.first())
            return JsonResponse({"registered": True, "user": user.name})
        return JsonResponse({"registered": False, "url": f"/register/{card_id}/"})

    except Wallet.DoesNotExist:
        return JsonResponse({"registered": False, "url": f"/register/{card_id}/"})


# Create your views here.


def index(request) -> HttpResponse:
    return render(request, "index.html")
