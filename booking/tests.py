from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import FitnessClass, Booking
from django.utils import timezone
from datetime import timedelta


class BookingTests(APITestCase):

    def setUp(self):
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            date_time=timezone.now() + timedelta(days=1),
            instructor="John",
            available_slots=10
        )

    def test_create_booking_success(self):
        url = reverse('book')
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Alice",
            "client_email": "a@a.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(FitnessClass.objects.get(id=self.fitness_class.id).available_slots, 9)

    def test_no_slots_available(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()

        url = reverse('book')
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Charlie",
            "client_email": "c@c.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["class_id"], ["No slots available."]
        )

    def test_create_duplicate_booking(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Alice",
            client_email="a@a.com"
        )
        url = reverse('book')
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Alice",
            "client_email": "a@a.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already booked", response.json()["error"])

    def test_booking_past_class(self):
        self.fitness_class.date_time = timezone.now() - timedelta(days=1)
        self.fitness_class.save()

        url = reverse('book')
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Bob",
            "client_email": "b@b.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["class_id"], ["Cannot book past classes."]
        )

    def test_invalid_class_id_booking(self):
        url = reverse('book')
        data = {
            "class_id": 9999,
            "client_name": "Daisy",
            "client_email": "d@d.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["class_id"], ["Class does not exist."]
        )
