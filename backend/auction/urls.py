from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf.urls.static import static
from django.conf import settings
from auction import views
from rest_framework.routers import DefaultRouter
from .views import AuctionViewSet

router = DefaultRouter()
router.register(r'auctions', AuctionViewSet)

urlpatterns: list[URLPattern] = [
    path('', views.index, name='index'),
]
