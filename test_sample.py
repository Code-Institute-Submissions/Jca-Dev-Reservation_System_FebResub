import django
django.setup()
from reservation_manager import models
import pytest
import manage


class Test_Reservation__generate_reservation_number:

    @pytest.fixture()
    def reservation(self):
        return models.Reservation()

    def test__generate_reservation_number_1(self, reservation):
        result = reservation._generate_reservation_number()


class Test_Reservation_Save:

    @pytest.fixture()
    def reservation(self):
        return models.Reservation(phone_number=1234567891, date_time='2023-02-01 18:40', party_size=1)

    def test_save_1(self, reservation):
        result = reservation.save(*[], **{})


class Test_Manage_Main:
    def test_main_1(self):
        result = manage.main()
