from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Base, max_seats, Reservation, UserProfile
from .forms import ReservationForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required


class Homepage(generic.ListView):
    model = Base
    template_name = 'homepage.html'


def Reservations(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            limbo = form.save(commit=False)
            seats = 0
            for data in Reservation.objects.all():
                if data.date_time - timedelta(hours=1) <= limbo.date_time and limbo.date_time <= data.date_time + timedelta(hours=1):
                    seats = seats + data.party_size
            seats_available = max_seats - seats
            if limbo.party_size <= seats_available:
                limbo.save()
                profile = UserProfile.objects.get(user=request.user)
                # Attach the user's profile to the reservation
                Reservation.user_profile = profile
                Reservation.save()
                return render(request, 'reservation_complete.html')
            else:
                messages.error(request, 'Sorry, there isnt enough seats available. please try another date/time.')
    else:
        form = ReservationForm()
    return render(request, 'reservation_page.html', {'form': form})


class Menu(generic.ListView):
    model = Base
    template_name = 'menu.html'


class Errors(generic.ListView):
    model = Base
    template_name = 'error_page.html'


class Rescomp(generic.ListView):
    model = Base
    template_name = 'reservation_complete.html'


@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    template = 'profile.html'
    reservations = profile.reservations.all()

    context = {
        'reservations': reservations,
    }

    return render(request, template, context)
