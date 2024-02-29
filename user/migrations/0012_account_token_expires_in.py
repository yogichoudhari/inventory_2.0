# Generated by Django 4.2.7 on 2024-02-27 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_userloggedinactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='token_expires_in',
            field=models.TimeField(default=datetime.time(0, 59)),
            preserve_default=False,
        ),
    ]
