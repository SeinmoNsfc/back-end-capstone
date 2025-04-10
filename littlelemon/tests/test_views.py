from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from restaurant.models import Menu, Booking
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from django.utils import timezone

class MenuViewTest(TestCase):
    def setUp(self):
        Menu.objects.create(title="Pizza", price=10.00, inventory=50)
        Menu.objects.create(title="Burger", price=8.00, inventory=30)

    def test_get_all(self):
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Pizza')
        self.assertEqual(response.data[1]['title'], 'Burger')

class BookingViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        # self.client.force_authenticate(user=self.user)

        self.url = reverse('booking-list')

        self.data = {
            'name': 'Lucas Smith',
            'no_of_guests': 2,
            'booking_date': timezone.now()
        }

    def test_create_booking(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().name, 'Lucas Smith')

    def test_list_bookings(self):
        Booking.objects.create(**self.data)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_permission_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
