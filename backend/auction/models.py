from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    name: models.CharField = models.CharField(max_length=50)
    surname: models.CharField = models.CharField(max_length=50)
    age: models.IntegerField = models.IntegerField()
    wallet: models.OneToOneField = models.OneToOneField(
        'Wallet', on_delete=models.CASCADE, related_name='user_wallet')

    def __str__(self):
        return f"{self.name} {self.surname}"


class Wallet(models.Model):
    card_id: models.CharField = models.CharField(max_length=50)
    balance: models.FloatField = models.FloatField()

    def __str__(self):
        return f"Wallet for {self.user.name}"


class Article(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    owner: models.ForeignKey = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    starting_price: models.FloatField = models.FloatField()
    description: models.TextField = models.TextField(default="")

    def __str__(self):
        return self.name


class Auction(models.Model):
    article: models.ForeignKey = models.ForeignKey(
        Article, on_delete=models.CASCADE)
    start_time: models.DateTimeField = models.DateTimeField(
        default=timezone.now)
    end_time: models.DateTimeField = models.DateTimeField(
        null=True, blank=True)
    is_active: models.BooleanField = models.BooleanField(default=False)
    current_price: models.FloatField = models.FloatField()

    def __str__(self):
        return f"Auction for {self.article.name}, current price: {self.current_price}, active: {self.is_active}"
