from django.urls import path

from auth import views

urlpatterns = [
    path("login", views.login, name="auth-login"),
    path("logout", views.logout, name="auth-logout"),
    path("logout-all", views.logout_all, name="auth-logout-all"),
]
