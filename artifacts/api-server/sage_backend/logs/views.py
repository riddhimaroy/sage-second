"""
Views for the logs app.
Handles daily food logging, weekly summaries, and auto-cleanup.
"""

from datetime import date, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from meals.models import Meal
from .models import DailyLog, LogEntry
from .serializers import DailyLogSerializer, WeeklySummarySerializer


def today_str():
    """Return today's date as a YYYY-MM-DD string."""
    return date.today().isoformat()


def get_or_create_daily_log(date_str):
    """
    Get or create a DailyLog for the given date string.
    Returns the DailyLog instance.
    """
    log, _ = DailyLog.objects.get_or_create(date=date_str)
    return log


def compute_totals(entries_qs):
    """
    Compute nutrition totals from a QuerySet of LogEntry objects.
    Multiplies each meal's per-serving values by the entry quantity.
    """
    totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fats": 0.0}
    for entry in entries_qs.select_related("meal"):
        q = entry.quantity
        totals["calories"] += entry.meal.calories * q
        totals["protein"] += entry.meal.protein * q
        totals["carbs"] += entry.meal.carbs * q
        totals["fats"] += entry.meal.fats * q
    return totals


@api_view(["GET"])
def get_today_log(request):
    """
    GET /api/logs/today
    Returns today's DailyLog with all entries and computed nutrition totals.
    Creates the daily log automatically if it doesn't exist yet.
    """
    daily_log = get_or_create_daily_log(today_str())
    serializer = DailyLogSerializer(daily_log)
    return Response(serializer.data)


@api_view(["POST"])
def add_log_entry(request):
    """
    POST /api/logs/add
    Body: { mealId: int, quantity: float }
    Add a meal to today's food log. Creates today's DailyLog if needed.
    """
    meal_id = request.data.get("mealId")
    quantity = request.data.get("quantity")

    # Validate inputs
    if meal_id is None or quantity is None:
        return Response({"error": "mealId and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return Response({"error": "quantity must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)

    # Verify the meal exists
    try:
        meal = Meal.objects.get(pk=meal_id)
    except Meal.DoesNotExist:
        return Response({"error": "Meal not found"}, status=status.HTTP_404_NOT_FOUND)

    daily_log = get_or_create_daily_log(today_str())
    entry = LogEntry.objects.create(meal=meal, daily_log=daily_log, quantity=quantity)

    return Response(
        {
            "id": entry.id,
            "mealId": entry.meal_id,
            "dailyLogId": entry.daily_log_id,
            "quantity": entry.quantity,
            "meal": {
                "id": meal.id,
                "name": meal.name,
                "calories": meal.calories,
                "protein": meal.protein,
                "carbs": meal.carbs,
                "fats": meal.fats,
                "servingSize": meal.serving_size,
                "category": meal.category,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["DELETE"])
def remove_log_entry(request, entry_id):
    """
    DELETE /api/logs/remove/<entry_id>
    Remove a specific log entry by its ID.
    """
    try:
        entry = LogEntry.objects.get(pk=entry_id)
    except LogEntry.DoesNotExist:
        return Response({"error": "Log entry not found"}, status=status.HTTP_404_NOT_FOUND)

    entry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
def update_log_entry(request, entry_id):
    """
    PATCH /api/logs/update/<entry_id>
    Body: { quantity: float }
    Update the quantity (serving size) of an existing log entry.
    """
    try:
        entry = LogEntry.objects.select_related("meal").get(pk=entry_id)
    except LogEntry.DoesNotExist:
        return Response({"error": "Log entry not found"}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get("quantity")
    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return Response({"error": "quantity must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)

    entry.quantity = quantity
    entry.save()
    meal = entry.meal

    return Response(
        {
            "id": entry.id,
            "mealId": entry.meal_id,
            "dailyLogId": entry.daily_log_id,
            "quantity": entry.quantity,
            "meal": {
                "id": meal.id,
                "name": meal.name,
                "calories": meal.calories,
                "protein": meal.protein,
                "carbs": meal.carbs,
                "fats": meal.fats,
                "servingSize": meal.serving_size,
                "category": meal.category,
            },
        }
    )


@api_view(["GET"])
def get_daily_logs(request):
    """
    GET /api/logs/daily?date=YYYY-MM-DD
    Returns the DailyLog for a specific date (defaults to today).
    """
    date_str = request.query_params.get("date", today_str())
    daily_log = get_or_create_daily_log(date_str)
    serializer = DailyLogSerializer(daily_log)
    return Response(serializer.data)


@api_view(["GET"])
def get_weekly_logs(request):
    """
    GET /api/logs/weekly
    Returns a 7-day summary: per-day totals, highest/lowest calorie days,
    average calories, and total days with logged entries.
    """
    # Build list of the last 7 days (oldest first)
    today = date.today()
    days = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]

    day_aggregates = []
    days_with_entries = []

    for day_str in days:
        try:
            log = DailyLog.objects.get(date=day_str)
            entries_qs = LogEntry.objects.filter(daily_log=log)
            totals = compute_totals(entries_qs)
            entry_count = entries_qs.count()
        except DailyLog.DoesNotExist:
            totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fats": 0.0}
            entry_count = 0

        agg = {
            "date": day_str,
            "entryCount": entry_count,
            **totals,
        }
        day_aggregates.append(agg)
        if entry_count > 0:
            days_with_entries.append(agg)

    # Determine highest and lowest calorie days
    highest_calorie_day = None
    lowest_calorie_day = None
    average_calories = 0.0

    if days_with_entries:
        sorted_days = sorted(days_with_entries, key=lambda d: d["calories"], reverse=True)
        highest_calorie_day = sorted_days[0]["date"]
        # Only set lowest if it's a different day from highest
        if len(sorted_days) > 1:
            lowest_calorie_day = sorted_days[-1]["date"]
        average_calories = sum(d["calories"] for d in days_with_entries) / len(days_with_entries)

    summary = {
        "days": day_aggregates,
        "highestCalorieDay": highest_calorie_day,
        "lowestCalorieDay": lowest_calorie_day,
        "averageCalories": round(average_calories, 1),
        "totalDaysLogged": len(days_with_entries),
    }

    serializer = WeeklySummarySerializer(summary)
    return Response(serializer.data)


@api_view(["POST"])
def cleanup_old_logs(request):
    """
    POST /api/logs/cleanup
    Deletes all DailyLog records (and their cascaded LogEntries) older than 7 days.
    Useful for keeping the database lean.
    """
    cutoff = (date.today() - timedelta(days=7)).isoformat()
    deleted_qs = DailyLog.objects.filter(date__lt=cutoff)
    count = deleted_qs.count()
    deleted_qs.delete()

    return Response(
        {
            "deletedLogs": count,
            "message": f"Deleted {count} log(s) older than 7 days",
        }
    )


@api_view(["GET"])
def get_daily_summary(request):
    """
    GET /api/summary/daily
    Returns today's total nutrition values (calories, protein, carbs, fats).
    Returns zeros if no meals have been logged today.
    """
    today = today_str()
    try:
        log = DailyLog.objects.get(date=today)
        totals = compute_totals(LogEntry.objects.filter(daily_log=log))
    except DailyLog.DoesNotExist:
        totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fats": 0.0}

    return Response(totals)
