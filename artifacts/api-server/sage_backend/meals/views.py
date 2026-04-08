"""
Views for the meals app.
Provides search and listing of available food items.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Meal
from .serializers import MealSerializer


@api_view(["GET"])
def health_check(request):
    """
    GET /api/healthz
    Simple health check endpoint.
    """
    return Response({"status": "ok"})


@api_view(["GET"])
def search_meals(request):
    """
    GET /api/meals/search?q=<query>
    Search meals by name (case-insensitive partial match).
    Returns up to 20 results.
    """
    q = request.query_params.get("q", "").strip()
    if not q:
        return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

    meals = Meal.objects.filter(name__icontains=q)[:20]
    serializer = MealSerializer(meals, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def list_meals(request):
    """
    GET /api/meals
    List all available meals ordered by name.
    """
    meals = Meal.objects.all()
    serializer = MealSerializer(meals, many=True)
    return Response(serializer.data)
