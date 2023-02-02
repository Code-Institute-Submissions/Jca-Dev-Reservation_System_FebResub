from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib import messages
from .models import Base, max_seats, Reservation, UserProfile
from .forms import ReservationForm
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required


class Homepage(generic.ListView):
    model = Base
    template_name = 'homepage.html'


@login_required
def Reservations(request):
    now = timezone.localtime()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            limbo = form.save(commit=False)
            seats = 0
            for data in Reservation.objects.all():
                # check the date and time are not in the past #
                if limbo.date_time < now:
                    messages.error(request, 'You cannot enter a date/time in the past.')
                    return render(request, 'reservation_page.html', {'form': form})
                # check the date, time and seats are available in that 1 hour window #
                if data.date_time - timedelta(hours=1) <= limbo.date_time and limbo.date_time <= data.date_time + timedelta(hours=1):
                    seats = seats + data.party_size
            seats_available = max_seats - seats
            if limbo.party_size <= seats_available:
                limbo.save()
                profile = UserProfile.objects.get(user=request.user)
                reservation = limbo
                reservation.user_profile = profile
                reservation.save()
                messages.success(request, 'Reservation Successfully Created')
                return redirect(reverse('rescomp', args=[reservation.reservation_number]))
            else:
                messages.error(request, 'Sorry, there are not enough seats available. please try another date/time.')
                return render(request, 'reservation_page.html', {'form': form})
    else:
        form = ReservationForm()
    return render(request, 'reservation_page.html', {'form': form})


def Reservations_success(request, reservation_number):
    reservation = get_object_or_404(Reservation, reservation_number=reservation_number)

    template = 'reservation_complete.html'
    context = {
        'reservation': reservation,
    }

    return render(request, template, context)


class Menu(generic.ListView):
    model = Base
    template_name = 'menu.html'


class Errors(generic.ListView):
    model = Base
    template_name = 'error_page.html'


@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    template = 'profile.html'
    reservations = profile.reservations.all()

    context = {
        'reservations': reservations,
        'profile': profile
    }

    return render(request, template, context)


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    now = timezone.localtime()
    seat = reservation.party_size
    if request.method == 'POST':
        form = ReservationForm(request.POST, request.FILES, instance=reservation)
        if form.is_valid():
            limbo = form.save(commit=False)
            seats = 0
            for data in Reservation.objects.all():
                if limbo.date_time < now:
                    messages.error(request, 'You cannot enter a date/time in the past.')
                    return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})
                if data.date_time - timedelta(hours=1) <= limbo.date_time and limbo.date_time <= data.date_time + timedelta(hours=1):
                    seats = seats + data.party_size - seat
            seats_available = max_seats - seats
            if limbo.party_size <= seats_available:
                limbo.save()
                messages.success(request, 'Reservation Successfully Changed')
                return redirect(reverse('profile'))
            else:
                messages.error(request, 'Sorry, there are not enough seats available. please try another date/time.')
                return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})
    else:
        form = ReservationForm(instance=reservation)

    template = 'edit_reservation.html'
    context = {
        'form': form,
        'reservation': reservation,
    }

    return render(request, template, context)


@login_required
def delete_reservation(request, reservation_id):

    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.delete()
    messages.success(request, 'Reservation Successfully Deleted')
    return redirect(reverse('profile'))
