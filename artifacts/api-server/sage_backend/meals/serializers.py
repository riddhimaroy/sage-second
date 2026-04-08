"""
Serializers for the Meal model.
"""

from rest_framework import serializers
from .models import Meal


class MealSerializer(serializers.ModelSerializer):
    """Serializes a Meal to/from JSON including all nutritional fields."""

    class Meta:
        model = Meal
        fields = ["id", "name", "calories", "protein", "carbs", "fats", "serving_size", "category"]
