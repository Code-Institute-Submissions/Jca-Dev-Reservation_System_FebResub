from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Base(models.Model):

    def __str__(self):
        return self.name

# ---------------------------------- Profile -------------------------#


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# ---------------------------------- Reservation -------------------------#


max_seats = 25


class Reservation(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='reservations')
    name = models.CharField(max_length=50)
    phone_number = models.IntegerField(error_messages={'invalid': 'Please enter a valid phone number'})
    party_size = models.IntegerField()
    date_time = models.DateTimeField()

    def __str__(self):
        return self.name
