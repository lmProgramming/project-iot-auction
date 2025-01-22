from django.shortcuts import render
from django.db.models.manager import BaseManager
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
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

from django.shortcuts import render
from .models import Auction
from django.contrib.auth.models import UserManager


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

    def perform_create(self, serializer) -> None:
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
    fields: list[str] = ["article", "start_time", "end_time", "current_price"]
    template_name = "auction_form.html"
    success_url = reverse_lazy("auction_list")


class ArticleCreateView(CreateView):
    model = Article
    fields: list[str] = ["name", "owner",
                         "starting_price", "description", "image"]
    template_name = "article_form.html"
    success_url = reverse_lazy("article_list")


class UserCreateView(CreateView):
    model = User
    fields: list[str] = ["name", "surname",
                         "login", "password", "age", "wallet"]
    template_name = "user_form.html"
    success_url = reverse_lazy("user_list")


class WalletCreateView(CreateView):
    model = Wallet
    fields: list[str] = ["card_id", "balance"]
    template_name = "wallet_form.html"
    success_url = reverse_lazy("wallet_list")


class UserWinsView(ListView):
    model = User
    template_name = "user_wins.html"


def manage_account(request, card_id: int) -> JsonResponse | None:
    wallet_qs = Wallet.objects.filter(card_id=card_id)
    if not wallet_qs.first():
        return JsonResponse({"error": "No user with such id"})
    user = User.objects.filter(wallet=wallet_qs.first())

    return JsonResponse({"user": user})


def register(request, card_id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
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


def check_registered(request, card_id: int) -> JsonResponse:
    try:
        wallet_qs = Wallet.objects.filter(card_id=card_id)
        if wallet_qs.exists():
            user: User = User.objects.get(wallet=wallet_qs.first())
            return JsonResponse({"registered": True, "user": user.name})
        return JsonResponse({"registered": False, "url": f"/register/{card_id}/"})

    except Wallet.DoesNotExist:
        return JsonResponse({"registered": False, "url": f"/register/{card_id}/"})


def user_wins_view(request) -> HttpResponse:
    user_wins: dict[User, list] = {user: [] for user in User.objects.all()}

    for auction in Auction.objects.filter(is_finished=True):
        print(auction)
        last_bidder = auction.last_bidder
        print(last_bidder)
        if last_bidder is None:
            continue
        assert isinstance(last_bidder, User)
        user_wins[last_bidder].append(auction)

    print(user_wins)

    return render(request, 'user_wins.html', {'users_with_wins': user_wins})


def index(request) -> HttpResponse:
    return render(request, "index.html")
