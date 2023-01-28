import uuid
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Base(models.Model):

    def __str__(self):
        return self.name

# ---------------------------------- Profile -------------------------#


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

# ---------------------------------- Reservation -------------------------#


max_seats = 25


class Reservation(models.Model):
    reservation_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='reservations')
    name = models.CharField(max_length=50)
    phone_number = models.IntegerField(error_messages={'invalid': 'Please enter a valid phone number'})
    party_size = models.IntegerField()
    date_time = models.DateTimeField()

    def _generate_reservation_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.reservation_number:
            self.reservation_number = self._generate_reservation_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reservation_number
