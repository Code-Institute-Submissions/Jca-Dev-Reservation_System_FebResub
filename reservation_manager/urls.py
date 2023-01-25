from . import views
from django.urls import path
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.Homepage.as_view(), name='home'),
    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
    path('reservation_page', views.Reservations, name='reservations'),
    path('menu', views.Menu.as_view(), name='menu'),
    path('reservation_complete/<reservation_number>', views.Reservations_success, name='rescomp'),
    path('profile', views.profile, name='profile'),
    path('edit_reservation', views.EditReservation, name='edit_reservation'),
]
