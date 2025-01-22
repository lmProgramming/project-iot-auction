# Generated by Django 5.1.5 on 2025-01-21 22:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0007_user_login_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='last_bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_auctions', to='auction.user'),
        ),
    ]