# Generated by Django 4.2.7 on 2024-01-31 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_account_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coupon_id',
            field=models.CharField(blank=True, max_length=33, null=True),
        ),
    ]
