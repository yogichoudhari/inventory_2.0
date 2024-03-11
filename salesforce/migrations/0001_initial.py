# Generated by Django 4.2.7 on 2024-03-11 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0016_alter_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptionKeyId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyid', models.CharField(max_length=256)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.account')),
            ],
        ),
        migrations.CreateModel(
            name='AccountCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.BinaryField()),
                ('client_secret', models.BinaryField()),
                ('base_url', models.URLField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.account')),
            ],
        ),
    ]