"""
URL patterns for the logs app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Today's log
    path("logs/today", views.get_today_log, name="logs-today"),

    # Add / remove / update log entries
    path("logs/add", views.add_log_entry, name="logs-add"),
    path("logs/remove/<int:entry_id>", views.remove_log_entry, name="logs-remove"),
    path("logs/update/<int:entry_id>", views.update_log_entry, name="logs-update"),

    # Daily and weekly views
    path("logs/daily", views.get_daily_logs, name="logs-daily"),
    path("logs/weekly", views.get_weekly_logs, name="logs-weekly"),

    # Cleanup old logs (older than 7 days)
    path("logs/cleanup", views.cleanup_old_logs, name="logs-cleanup"),

    # Daily nutrition summary
    path("summary/daily", views.get_daily_summary, name="summary-daily"),
]
