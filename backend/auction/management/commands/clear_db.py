from django.core.management.base import BaseCommand
from auction.models import User, Article, Auction, Wallet


class Command(BaseCommand):
    help = 'Clears the database'

    def handle(self, *args, **kwargs) -> None:
        User.objects.all().delete()
        Article.objects.all().delete()
        Auction.objects.all().delete()
        Wallet.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Database cleared successfully'))
