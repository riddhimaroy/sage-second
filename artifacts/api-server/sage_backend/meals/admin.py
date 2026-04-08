from django.contrib import admin

from .models import Meal


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "calories", "protein", "carbs", "fats", "serving_size")
    list_filter = ("category",)
    search_fields = ("name", "category")
    ordering = ("name",)
