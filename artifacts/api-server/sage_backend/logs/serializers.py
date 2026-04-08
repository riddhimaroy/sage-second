"""
Serializers for the logs app.
"""

from rest_framework import serializers
from meals.serializers import MealSerializer
from .models import DailyLog, LogEntry


class LogEntrySerializer(serializers.ModelSerializer):
    """Serializes a LogEntry including its nested Meal data."""
    meal = MealSerializer(read_only=True)
    mealId = serializers.IntegerField(source="meal_id", read_only=True)
    dailyLogId = serializers.IntegerField(source="daily_log_id", read_only=True)

    class Meta:
        model = LogEntry
        fields = ["id", "mealId", "dailyLogId", "quantity", "meal"]


class NutritionTotalsSerializer(serializers.Serializer):
    """Computed nutrition totals across all log entries."""
    calories = serializers.FloatField()
    protein = serializers.FloatField()
    carbs = serializers.FloatField()
    fats = serializers.FloatField()


class DailyLogSerializer(serializers.ModelSerializer):
    """Serializes a DailyLog with its entries and computed totals."""
    # REPLACED
    entries = serializers.SerializerMethodField()
    totals = serializers.SerializerMethodField()

    class Meta:
        model = DailyLog
        fields = ["id", "date", "entries", "totals"]

    def _get_user_scoped_entries(self, obj):
        """
        Always scope serialized entries to the DailyLog owner first so a shared
        serializer context can never leak another user's rows.
        """
        entries_qs = obj.entries.select_related("meal").filter(user=obj.user)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            entries_qs = entries_qs.filter(user=request.user)
        return entries_qs

    def get_entries(self, obj):
        return LogEntrySerializer(self._get_user_scoped_entries(obj), many=True).data

    def get_totals(self, obj):
        """Compute the sum of calories, protein, carbs, fats for all entries."""
        totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fats": 0.0}
        for entry in self._get_user_scoped_entries(obj):
            q = entry.quantity
            totals["calories"] += entry.meal.calories * q
            totals["protein"] += entry.meal.protein * q
            totals["carbs"] += entry.meal.carbs * q
            totals["fats"] += entry.meal.fats * q
        return totals


class DayAggregateSerializer(serializers.Serializer):
    """Per-day nutrition aggregate for the weekly summary."""
    date = serializers.CharField()
    calories = serializers.FloatField()
    protein = serializers.FloatField()
    carbs = serializers.FloatField()
    fats = serializers.FloatField()
    entryCount = serializers.IntegerField()


class WeeklySummarySerializer(serializers.Serializer):
    """Full 7-day summary including per-day aggregates and stats."""
    days = DayAggregateSerializer(many=True)
    highestCalorieDay = serializers.CharField(allow_null=True)
    lowestCalorieDay = serializers.CharField(allow_null=True)
    averageCalories = serializers.FloatField()
    totalDaysLogged = serializers.IntegerField()
