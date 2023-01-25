from django.contrib import admin
from .models import Reservation, UserProfile


@admin.register(Reservation)
class admin_display(admin.ModelAdmin):

    list_display = ['name', 'date_time', 'user_profile', 'reservation_number']
    list_filter = ['name', 'date_time', 'user_profile', 'reservation_number']
    search_fields = ['name', 'date_time', 'user_profile', 'reservation_number']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'id',
    )
