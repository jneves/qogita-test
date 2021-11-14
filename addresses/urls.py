from django.urls import path

from addresses import views


urlpatterns = [
    path("", views.AddressList.as_view(), name="address-list"),
    path("<uuid:pk>/", views.AddressDetail.as_view(), name="address-detail"),
]
