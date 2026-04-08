"""
UserProfile model — extends Django's built-in User with nutrition profile data.
"""

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ACTIVITY_CHOICES = [
        ("sedentary", "Sedentary"),
        ("light", "Light"),
        ("moderate", "Moderate"),
        ("active", "Active"),
    ]
    GOAL_CHOICES = [
        ("lose", "Lose Weight"),
        ("maintain", "Maintain Weight"),
        ("gain", "Gain Weight"),
    ]
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    height_cm = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, null=True, blank=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, null=True, blank=True)
    custom_protein_g = models.FloatField(null=True, blank=True)
    use_custom_protein = models.BooleanField(default=False)

    class Meta:
        db_table = "django_user_profiles"

    def __str__(self):
        return f"Profile of {self.user.username}"

    def is_complete(self):
        return all([self.age, self.gender, self.height_cm, self.weight_kg,
                    self.activity_level, self.goal])
