from django.core.management.base import BaseCommand
from auction.models import User, Article, Auction, Wallet


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs) -> None:
        # Create wallets
        wallet1: Wallet = Wallet.objects.create(card_id="1", balance=1000)
        wallet2: Wallet = Wallet.objects.create(card_id="2", balance=2000)

        # Create users
        user1: User = User.objects.create(
            name="John",
            surname="Doe",
            age=30,
            wallet=wallet1,
            login="john_doe",
            password="password",
        )
        user2: User = User.objects.create(
            name="Jane",
            surname="Doe",
            age=25,
            wallet=wallet2,
            login="jane_doe",
            password="password",
        )

        # Create articles
        article1: Article = Article.objects.create(
            name="Laptop", starting_price=500, owner=user1
        )
        article2: Article = Article.objects.create(
            name="Phone", starting_price=300, owner=user2
        )

        # Create auctions
        Auction.objects.create(article=article1, is_active=True, current_price=500)
        Auction.objects.create(article=article2, is_active=False, current_price=300)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
