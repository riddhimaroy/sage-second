"""
Meal model — stores nutritional information for each food item.
"""

from django.db import models


class Meal(models.Model):
    """
    Represents a food item with its nutritional data per serving.
    Used as the source for meal search and logging.
    """
    name = models.CharField(max_length=255, help_text="Display name of the food item")
    calories = models.FloatField(help_text="Calories per serving")
    protein = models.FloatField(help_text="Protein in grams per serving")
    carbs = models.FloatField(help_text="Carbohydrates in grams per serving")
    fats = models.FloatField(help_text="Fats in grams per serving")
    serving_size = models.CharField(max_length=100, default="100g", help_text="Description of one serving")
    category = models.CharField(max_length=100, default="General", help_text="Food category (e.g. Protein, Grains)")

    class Meta:
        db_table = "django_meals"   # Distinct from legacy Drizzle 'meals' table
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"
