# Generated by Django 3.2.16 on 2023-01-18 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0007_auto_20230118_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='user_profile',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservation_manager.userprofile'),
        ),
    ]