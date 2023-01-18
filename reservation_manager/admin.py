from django.contrib import admin
from .models import Reservation, UserProfile


@admin.register(Reservation)
class admin_display(admin.ModelAdmin):

    list_display = ['name', 'date_time', 'user_profile']
    list_filter = ['name', 'date_time', 'user_profile']
    search_fields = ['name', 'date_time', 'user_profile']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )
