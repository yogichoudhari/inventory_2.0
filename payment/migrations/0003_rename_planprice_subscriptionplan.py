# Generated by Django 4.2.7 on 2024-01-17 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_subscription_planprice'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlanPrice',
            new_name='SubscriptionPlan',
        ),
    ]