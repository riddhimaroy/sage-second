from django.contrib import admin

from .models import DailyLog, LogEntry


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "created_at")
    list_filter = ("date", "user")
    search_fields = ("user__username", "date")
    ordering = ("-date", "-id")


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "daily_log", "meal", "quantity", "created_at")
    list_filter = ("user", "meal__category", "created_at")
    search_fields = ("user__username", "meal__name", "daily_log__date")
    ordering = ("-id",)
