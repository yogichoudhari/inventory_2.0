# Generated by Django 4.2.7 on 2024-02-26 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_rename_roll_role_rename_roll_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLoggedInActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_status', models.CharField(choices=[('success', 'success'), ('failed', 'failed')], max_length=8)),
                ('ip_address', models.GenericIPAddressField()),
                ('login_datetime', models.DateTimeField(auto_now=True)),
                ('user_agent_info', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
