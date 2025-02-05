# Generated by Django 5.1.4 on 2025-01-08 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='item',
            new_name='article',
        ),
        migrations.RemoveField(
            model_name='article',
            name='current_price',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='user',
        ),
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='auction',
            name='current_price',
            field=models.FloatField(default=100),
            preserve_default=False,
        ),
    ]
