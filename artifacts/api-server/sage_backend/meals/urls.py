"""
URL patterns for the meals app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path("healthz", views.health_check, name="health-check"),

    # Meal search and listing
    path("meals/search", views.search_meals, name="meals-search"),
    path("meals", views.list_meals, name="meals-list"),
]
