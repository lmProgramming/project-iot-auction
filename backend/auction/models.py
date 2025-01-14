from datetime import timedelta
from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    name: models.CharField = models.CharField(max_length=50)
    surname: models.CharField = models.CharField(max_length=50)
    login: models.CharField = models.CharField(max_length=50, unique=True)
    password: models.CharField = models.CharField(max_length=50)
    age: models.IntegerField = models.IntegerField()
    wallet: models.OneToOneField = models.OneToOneField(
        "Wallet", on_delete=models.CASCADE, related_name="user_wallet"
    )

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
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    starting_price: models.FloatField = models.FloatField()
    description: models.TextField = models.TextField(default="")
    image: models.ImageField = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name


class Auction(models.Model):
    article: models.ForeignKey = models.ForeignKey(Article, on_delete=models.CASCADE)
    start_time: models.DateTimeField = models.DateTimeField(default=timezone.now)
    end_time: models.DateTimeField = models.DateTimeField(null=True, blank=True)
    is_active: models.BooleanField = models.BooleanField(default=False)
    is_finished: models.BooleanField = models.BooleanField(default=False)
    current_price: models.FloatField = models.FloatField()
    last_bidder = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="last_bid_auction",
    )

    def __str__(self):
        return f"Auction for {self.article.name}, current price: {self.current_price}, active: {self.is_active}"

    def start_auction(self):
        """Start the auction."""
        self.is_active = True
        self.end_time = timezone.now() + timedelta(minutes=1)
        self.is_finished = False
        self.save()

    def extend_time(self, seconds=15):
        if self.is_active:
            self.end_time = timezone.now() + timedelta(seconds=seconds)
            self.save()

    def finish_auction(self):
        """Mark the auction as finished."""
        self.is_finished = True
        self.is_active = False
        if self.last_bidder:
            self.last_bidder.wallet.balance -= self.current_price
            self.last_bidder.wallet.save()
        self.save()

    def bid(self, card_uuid: str, amount=20):
        """Place a bid on the auction."""
        if not self.is_active:
            raise ValueError("Auction is not active.")
        wallet = Wallet.objects.get(card_id=card_uuid)
        if not wallet:
            raise ValueError("Wallet not found.")
        if wallet.balance < self.current_price + amount:
            raise ValueError("Insufficient funds to place a bid.")
        bidder = User.objects.get(wallet=wallet)
        if not bidder:
            raise ValueError("User not found.")
        Bid.objects.create(
            auction=self, bidder=bidder, amount=self.current_price + amount
        )
        self.last_bidder = bidder
        self.current_price += amount
        self.extend_time(seconds=10)

    def create_payload(self, event: str):

        article = self.article
        return {
            "event": event,
            "auction": {
                "id": self.id,
                "name": article.name,
                "description": article.name,
                "price": self.current_price,
                "ends_in": (self.end_time - timezone.now()).seconds,
            },
        }


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.bidder.name} on {self.auction.article.name} for {self.amount}"

    def save(self, *args, **kwargs):
        if self.amount <= self.auction.current_price:
            raise ValueError("Bid must be higher than the current price.")

        if not self.auction.is_active:
            raise ValueError("Cannot place a bid on an inactive auction.")

        # Update auction current price and last bidder
        self.auction.current_price = self.amount
        self.auction.last_bidder = self.bidder
        self.auction.extend_time(seconds=10)  # Extend the auction
        self.auction.save()

        super().save(*args, **kwargs)
