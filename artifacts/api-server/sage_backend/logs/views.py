"""
Views for the logs app.
Handles daily food logging, weekly summaries, and auto-cleanup.
"""

from datetime import date, timedelta
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from meals.models import Meal
from .models import DailyLog, LogEntry
from .serializers import DailyLogSerializer, WeeklySummarySerializer


def parse_positive_integer_quantity(raw_quantity):
    """Validate that quantity is a positive integer serving count."""
    try:
        quantity = float(raw_quantity)
    except (TypeError, ValueError):
        raise ValueError("quantity must be a positive integer")

    if not quantity.is_integer() or quantity <= 0:
        raise ValueError("quantity must be a positive integer")

    return int(quantity)


def today_str():
    """Return today's date as a YYYY-MM-DD string."""
    return date.today().isoformat()


def get_or_create_daily_log(user, date_str):
    """
    Get or create a DailyLog for the given date string.
    Returns the DailyLog instance.
    """
    # FIXED: make daily logs user-specific
    log, _ = DailyLog.objects.get_or_create(user=user, date=date_str)
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_today_log(request):
    """
    GET /api/logs/today
    Returns today's DailyLog with all entries and computed nutrition totals.
    Creates the daily log automatically if it doesn't exist yet.
    """
    # FIXED: fetch today's log for the logged-in user only
    daily_log = get_or_create_daily_log(request.user, today_str())
    serializer = DailyLogSerializer(daily_log, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_log_entry(request):
    """
    POST /api/logs/add
    Body: { mealId: int, quantity: int }
    Add a meal to today's food log. Creates today's DailyLog if needed.
    """
    meal_id = request.data.get("mealId")
    quantity = request.data.get("quantity")

    # Validate inputs
    if meal_id is None or quantity is None:
        return Response({"error": "mealId and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        quantity = parse_positive_integer_quantity(quantity)
    except ValueError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    # Verify the meal exists
    try:
        meal = Meal.objects.get(pk=meal_id)
    except Meal.DoesNotExist:
        return Response({"error": "Meal not found"}, status=status.HTTP_404_NOT_FOUND)

    # FIXED: create entry inside the current user's daily log
    daily_log = get_or_create_daily_log(request.user, today_str())
    # FIXED: tie each entry directly to the logged-in user
    entry = LogEntry.objects.create(user=request.user, meal=meal, daily_log=daily_log, quantity=quantity)

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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_log_entry(request, entry_id):
    """
    DELETE /api/logs/remove/<entry_id>
    Remove a specific log entry by its ID.
    """
    try:
        # FIXED: only allow deleting the logged-in user's entry
        entry = LogEntry.objects.get(pk=entry_id, daily_log__user=request.user, user=request.user)
    except LogEntry.DoesNotExist:
        return Response({"error": "Log entry not found"}, status=status.HTTP_404_NOT_FOUND)

    entry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_log_entry(request, entry_id):
    """
    PATCH /api/logs/update/<entry_id>
    Body: { quantity: int }
    Update the quantity (serving size) of an existing log entry.
    """
    try:
        # FIXED: only allow updating the logged-in user's entry
        entry = LogEntry.objects.select_related("meal").get(pk=entry_id, daily_log__user=request.user, user=request.user)
    except LogEntry.DoesNotExist:
        return Response({"error": "Log entry not found"}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get("quantity")
    try:
        quantity = parse_positive_integer_quantity(quantity)
    except ValueError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_daily_logs(request):
    """
    GET /api/logs/daily?date=YYYY-MM-DD
    Returns the DailyLog for a specific date (defaults to today).
    """
    date_str = request.query_params.get("date", today_str())
    # FIXED: fetch the requested date for the logged-in user only
    daily_log = get_or_create_daily_log(request.user, date_str)
    serializer = DailyLogSerializer(daily_log, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
            # FIXED: summary must only include the logged-in user's logs
            log = DailyLog.objects.get(user=request.user, date=day_str)
            entries_qs = LogEntry.objects.filter(daily_log=log, user=request.user)
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cleanup_old_logs(request):
    """
    POST /api/logs/cleanup
    Deletes all DailyLog records (and their cascaded LogEntries) older than 7 days.
    Useful for keeping the database lean.
    """
    cutoff = (date.today() - timedelta(days=7)).isoformat()
    # FIXED: only delete old logs belonging to the logged-in user
    deleted_qs = DailyLog.objects.filter(user=request.user, date__lt=cutoff)
    count = deleted_qs.count()
    deleted_qs.delete()

    return Response(
        {
            "deletedLogs": count,
            "message": f"Deleted {count} log(s) older than 7 days",
        }
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_daily_summary(request):
    """
    GET /api/summary/daily
    Returns today's total nutrition values (calories, protein, carbs, fats).
    Returns zeros if no meals have been logged today.
    """
    today = today_str()
    try:
        # FIXED: summary must be user-specific
        log = DailyLog.objects.get(user=request.user, date=today)
        totals = compute_totals(LogEntry.objects.filter(daily_log=log, user=request.user))
    except DailyLog.DoesNotExist:
        totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fats": 0.0}

    return Response(totals)
