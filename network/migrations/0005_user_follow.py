# Generated by Django 5.0.3 on 2024-04-30 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_user_signed_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.BooleanField(default=False),
        ),
    ]