"""
URL configuration for SAGE backend.
All routes are served under the /api/ prefix.
"""

from django.urls import path, include

urlpatterns = [
    # All API endpoints live under /api/
    path("api/", include("meals.urls")),
    path("api/", include("logs.urls")),
    path("api/", include("users.urls")),
]
