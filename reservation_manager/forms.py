from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    INTEGER_CHOICES = [tuple([x, x]) for x in range(1, 26)]
    name = forms.CharField()
    phone_number = forms.CharField(label='Phone', min_length=1, max_length=11)
    party_size = forms.ChoiceField(choices=INTEGER_CHOICES)

    class Meta:
        model = Reservation
        fields = ['name', 'phone_number', 'date_time', 'party_size']
        widgets = {
            'date_time': DateTimePickerInput(),
        }
