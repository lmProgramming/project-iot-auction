from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf.urls.static import static
from django.conf import settings
from auction import views
from rest_framework.routers import DefaultRouter
from .views import AuctionViewSet
from django.contrib.auth.views import LoginView

router = DefaultRouter()
router.register(r"auctions", AuctionViewSet)

urlpatterns: list[URLPattern] = [
    path("", views.index, name="index"),
    path("create_article/", views.create_article, name="create_article"),
    path("register/<str:card_id>/", views.register, name="register"),
]
