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
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wallet_user')
    card_id: models.CharField = models.CharField(max_length=50)
    balance: models.FloatField = models.FloatField()

    def __str__(self):
        return f"Wallet for {self.user.name}"


class Article(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    starting_price: models.FloatField = models.FloatField()
    current_price: models.FloatField = models.FloatField()
    owner: models.ForeignKey = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Auction(models.Model):
    item: models.ForeignKey = models.ForeignKey(
        Article, on_delete=models.CASCADE)
    start_time: models.DateTimeField = models.DateTimeField(
        default=timezone.now)
    end_time: models.DateTimeField = models.DateTimeField(
        null=True, blank=True)
    is_active: models.BooleanField = models.BooleanField(default=False)

    def __str__(self):
        return f"Auction for {self.item.name}"
