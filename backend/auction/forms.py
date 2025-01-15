from django import forms
from .models import Article, User


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["name", "owner", "starting_price", "description", "image"]


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "age", "login", "password"]
