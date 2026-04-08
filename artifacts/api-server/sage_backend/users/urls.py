from django.urls import path
from . import views

urlpatterns = [
    path("auth/register", views.register),
    path("auth/login", views.login_view),
    path("auth/logout", views.logout_view),
    path("auth/profile", views.profile_view),
]
