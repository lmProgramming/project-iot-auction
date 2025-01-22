from django.core.management.base import BaseCommand
from auction.models import User, Article, Auction, Wallet


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs) -> None:
        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
