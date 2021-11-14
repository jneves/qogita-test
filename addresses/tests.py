from rest_framework import status
from rest_framework.test import APITestCase

from addresses.models import Address


class TestAddressCase(APITestCase):
    def test_create_address(self):
        """
        Ensure we can create a new address object.
        """
        data = {
            "country": "PT",
            "postal_code": "1000-260",
            "city": "Lisboa",
            "street_address": "Av. João XXI, 23 - 5Dto",
        }
        response = self.client.post("/addresses", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.get().postal_code, "1000-260")
