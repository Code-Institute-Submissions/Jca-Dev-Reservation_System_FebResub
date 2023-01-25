from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib import messages
from .models import Base, max_seats, Reservation, UserProfile
from .forms import ReservationForm, EditReservationForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required


class Homepage(generic.ListView):
    model = Base
    template_name = 'homepage.html'


@login_required
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
                reservation = limbo
                reservation.user_profile = profile
                reservation.save()
                return redirect(reverse('rescomp', args=[reservation.reservation_number]))
            else:
                messages.error(request, 'Sorry, there isnt enough seats available. please try another date/time.')
    else:
        form = ReservationForm()
    return render(request, 'reservation_page.html', {'form': form})


def Reservations_success(request, reservation_number):
    reservation = get_object_or_404(Reservation, reservation_number=reservation_number)
    print(reservation_number)

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
    print(profile)

    context = {
        'reservations': reservations,
        'profile': profile
    }

    return render(request, template, context)


@login_required
def EditReservation(request, Reservation_id):

    reservation = get_object_or_404(Reservation, pk=Reservation_id)
    if request.method == 'POST':
        form = EditReservationForm(request.POST, request.FILES, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', args=[Reservation.id]))
        else:
            messages.error(request, 'Sorry, there isnt enough seats available. please try another date/time.')
    else:
        form = ReservationForm()

    template = 'edit_reservation.html'
    context = {
        'form': form,
        'reservation': reservation,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.info(request, 'Product deleted!')
    return redirect(reverse('products'))