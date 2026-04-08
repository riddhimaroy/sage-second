from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "age",
        "gender",
        "height_cm",
        "weight_kg",
        "activity_level",
        "goal",
        "use_custom_protein",
    )
    list_filter = ("gender", "activity_level", "goal", "use_custom_protein")
    search_fields = ("user__username",)
