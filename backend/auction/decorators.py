# decorators.py
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Wallet


def check_card_registration(fun):
    def wrapper(request, card_id, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(card_id=card_id)
            print("Card found")
            if wallet:
                return fun(request, card_id, *args, **kwargs)
            else:
                print("Card not found")
                return redirect("register", card_id=card_id)
        except Wallet.DoesNotExist:
            print("Card not found")
            return redirect("register", card_id=card_id)

    return wrapper
