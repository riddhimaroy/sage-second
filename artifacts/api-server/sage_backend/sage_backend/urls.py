"""
URL configuration for SAGE backend.
All routes are served under the /api/ prefix.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # All API endpoints live under /api/
    path("api/", include("meals.urls")),
    path("api/", include("logs.urls")),
    path("api/", include("users.urls")),
]
