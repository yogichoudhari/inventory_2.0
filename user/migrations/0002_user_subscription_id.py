# Generated by Django 4.2.7 on 2024-01-17 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscription_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
