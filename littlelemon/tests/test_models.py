from django.test import TestCase
from restaurant.models import Menu, Booking
from django.utils import timezone

class MenuItemTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)

        self.assertEqual(str(item), "IceCream : 80")

class BookingModelTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            name="Lucas Smith",
            no_of_guests=4,
            booking_date=timezone.now()
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.name, "Lucas Smith")
        self.assertEqual(self.booking.no_of_guests, 4)
        self.assertIsNotNone(self.booking.booking_date)

    def test_str_representation(self):
        expected_str = f"Booking by {self.booking.name} for {self.booking.no_of_guests} guests on {self.booking.booking_date}"
        self.assertEqual(str(self.booking), expected_str)
