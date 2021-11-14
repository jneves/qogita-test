from django.urls import include, path

from backend.views import api_root

urlpatterns = [
    path("", api_root),
    path("addresses/v1/", include("addresses.urls")),
    path("auth/v1/", include("auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
