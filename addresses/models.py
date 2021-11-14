import uuid

from django.conf import settings
from django.db import models
from pycountry import countries

COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in countries]


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # Fields compatible with the Google i18n definitions
    country_code = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    country_area = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    city_area = models.CharField(max_length=200)
    street_address = models.TextField()
    postal_code = models.CharField(max_length=200)
    sorting_code = models.CharField(max_length=200)

    class Meta:
        ordering = ["created"]
