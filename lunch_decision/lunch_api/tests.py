from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantTests(APITestCase):
    def setUp(self):
        self.restaurant1 = Restaurant.objects.create(
            name="Restaurant 1",
            address="123 Main St",
            phone_number="555-555-5555"
        )
        self.restaurant2 = Restaurant.objects.create(
            name="Restaurant 2",
            address="456 Elm St",
            phone_number="555-555-5555"
        )
        self.url = reverse('restaurant-list')

    def test_get_restaurants(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = RestaurantSerializer([self.restaurant1, self.restaurant2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_create_restaurant(self):
        data = {
            'name': 'New Restaurant',
            'address': '789 Oak St',
            'phone_number': '555-555-5555',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 3)
        self.assertEqual(Restaurant.objects.get(name='New Restaurant').address, '789 Oak St')
