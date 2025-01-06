from django.db import models

# Create your models here.


class User(models.Model):
    name: models.CharField = models.CharField(max_length=50)
    surname: models.CharField = models.CharField(max_length=50)
    age: models.IntegerField = models.IntegerField()
    wallet: models.OneToOneField = models.OneToOneField(
        'Wallet', on_delete=models.CASCADE)


class Wallet(models.Model):
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    rfid_id: models.CharField = models.CharField(max_length=50)
    balance: models.FloatField = models.FloatField()
