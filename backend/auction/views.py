from django.shortcuts import render
from django.db.models.manager import BaseManager
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Auction, Article, User
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

# Create your views here.


def index(request) -> HttpResponse:
    return render(request, 'index.html')
