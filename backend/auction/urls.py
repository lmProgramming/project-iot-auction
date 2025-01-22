from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf.urls.static import static
from django.conf import settings
from auction import views
from rest_framework.routers import DefaultRouter
from .views import (
    AuctionViewSet,
    AuctionListView,
    ArticleListView,
    UserListView,
    WalletListView,
    AuctionCreateView,
    ArticleCreateView,
    UserCreateView,
    WalletCreateView,
    UserWinsView
)
from django.contrib.auth.views import LoginView

router = DefaultRouter()
router.register(r"auctions", AuctionViewSet)

urlpatterns: list[URLPattern] = [
    path("", views.index, name="index"),
    path("register/<str:card_id>/", views.register, name="register"),
    path("auctions/", AuctionListView.as_view(), name="auction_list"),
    path("articles/", ArticleListView.as_view(), name="article_list"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("wallets/", WalletListView.as_view(), name="wallet_list"),
    path("create_auction/", AuctionCreateView.as_view(), name="create_auction"),
    path("create_article/", ArticleCreateView.as_view(), name="create_article"),
    path("create_user/", UserCreateView.as_view(), name="create_user"),
    path("create_wallet/", WalletCreateView.as_view(), name="create_wallet"),
    path("check_registered/<str:card_id>/",
         views.check_registered, name="check_registered"),
    path("user_wins/", views.user_wins_view, name="user_wins")
]
