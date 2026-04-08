"""
Management command to seed the meals database with sample food items.
Run with: python manage.py seed_meals
"""

from django.core.management.base import BaseCommand
from meals.models import Meal


SAMPLE_MEALS = [
    # ── Protein sources ────────────────────────────────────────────────────────
    {"name": "Grilled Chicken Breast", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "serving_size": "100g", "category": "Protein"},
    {"name": "Salmon Fillet", "calories": 208, "protein": 28, "carbs": 0, "fats": 10, "serving_size": "100g", "category": "Protein"},
    {"name": "Scrambled Eggs", "calories": 148, "protein": 10, "carbs": 1.6, "fats": 11, "serving_size": "2 eggs", "category": "Protein"},
    {"name": "Tuna (canned in water)", "calories": 132, "protein": 29, "carbs": 0, "fats": 1, "serving_size": "100g", "category": "Protein"},
    {"name": "Turkey Breast (roasted)", "calories": 135, "protein": 26, "carbs": 0, "fats": 3, "serving_size": "100g", "category": "Protein"},
    {"name": "Beef Steak (lean)", "calories": 217, "protein": 26, "carbs": 0, "fats": 12, "serving_size": "100g", "category": "Protein"},
    # ── Grains ─────────────────────────────────────────────────────────────────
    {"name": "Brown Rice", "calories": 216, "protein": 5, "carbs": 45, "fats": 1.8, "serving_size": "1 cup cooked", "category": "Grains"},
    {"name": "Whole Grain Toast", "calories": 138, "protein": 5.4, "carbs": 24, "fats": 2.4, "serving_size": "2 slices", "category": "Grains"},
    {"name": "Oatmeal", "calories": 150, "protein": 5, "carbs": 27, "fats": 3, "serving_size": "1/2 cup dry", "category": "Grains"},
    {"name": "Pasta (whole wheat)", "calories": 174, "protein": 7.5, "carbs": 37, "fats": 0.8, "serving_size": "1 cup cooked", "category": "Grains"},
    {"name": "Quinoa", "calories": 222, "protein": 8, "carbs": 39, "fats": 3.5, "serving_size": "1 cup cooked", "category": "Grains"},
    # ── Vegetables ─────────────────────────────────────────────────────────────
    {"name": "Steamed Broccoli", "calories": 55, "protein": 3.7, "carbs": 11, "fats": 0.6, "serving_size": "1 cup", "category": "Vegetables"},
    {"name": "Sweet Potato", "calories": 130, "protein": 3, "carbs": 30, "fats": 0.1, "serving_size": "1 medium", "category": "Vegetables"},
    {"name": "Spinach", "calories": 23, "protein": 2.9, "carbs": 3.6, "fats": 0.4, "serving_size": "100g raw", "category": "Vegetables"},
    {"name": "Bell Pepper", "calories": 31, "protein": 1, "carbs": 7, "fats": 0.3, "serving_size": "1 medium", "category": "Vegetables"},
    # ── Fruits ─────────────────────────────────────────────────────────────────
    {"name": "Banana", "calories": 105, "protein": 1.3, "carbs": 27, "fats": 0.4, "serving_size": "1 medium", "category": "Fruit"},
    {"name": "Apple", "calories": 95, "protein": 0.5, "carbs": 25, "fats": 0.3, "serving_size": "1 medium", "category": "Fruit"},
    {"name": "Avocado", "calories": 160, "protein": 2, "carbs": 9, "fats": 15, "serving_size": "1/2 medium", "category": "Fruit"},
    {"name": "Strawberries", "calories": 49, "protein": 1, "carbs": 12, "fats": 0.5, "serving_size": "1 cup", "category": "Fruit"},
    {"name": "Blueberries", "calories": 84, "protein": 1.1, "carbs": 21, "fats": 0.5, "serving_size": "1 cup", "category": "Fruit"},
    {"name": "Orange", "calories": 62, "protein": 1.2, "carbs": 15, "fats": 0.2, "serving_size": "1 medium", "category": "Fruit"},
    # ── Dairy ──────────────────────────────────────────────────────────────────
    {"name": "Greek Yogurt", "calories": 100, "protein": 17, "carbs": 6, "fats": 0.7, "serving_size": "170g", "category": "Dairy"},
    {"name": "Cottage Cheese", "calories": 110, "protein": 12, "carbs": 4, "fats": 5, "serving_size": "100g", "category": "Dairy"},
    {"name": "Whole Milk", "calories": 149, "protein": 8, "carbs": 12, "fats": 8, "serving_size": "1 cup", "category": "Dairy"},
    {"name": "Cheddar Cheese", "calories": 113, "protein": 7, "carbs": 0.4, "fats": 9, "serving_size": "28g / 1 oz", "category": "Dairy"},
    # ── Legumes ────────────────────────────────────────────────────────────────
    {"name": "Lentil Soup", "calories": 140, "protein": 9, "carbs": 24, "fats": 0.4, "serving_size": "1 cup", "category": "Legumes"},
    {"name": "Black Beans", "calories": 227, "protein": 15, "carbs": 41, "fats": 0.9, "serving_size": "1 cup cooked", "category": "Legumes"},
    {"name": "Hummus", "calories": 166, "protein": 8, "carbs": 14, "fats": 9.6, "serving_size": "100g", "category": "Legumes"},
    # ── Nuts ───────────────────────────────────────────────────────────────────
    {"name": "Almonds", "calories": 164, "protein": 6, "carbs": 6, "fats": 14, "serving_size": "28g / 1 oz", "category": "Nuts"},
    {"name": "Peanut Butter", "calories": 188, "protein": 8, "carbs": 6, "fats": 16, "serving_size": "2 tbsp", "category": "Nuts"},

    # ══════════════════════════════════════════════════════════════════════════
    # INDIAN FOOD
    # ══════════════════════════════════════════════════════════════════════════

    # ── Indian Breakfast ───────────────────────────────────────────────────────
    {"name": "Idli (steamed rice cake)", "calories": 58, "protein": 2, "carbs": 12, "fats": 0.4, "serving_size": "1 piece (50g)", "category": "Indian Breakfast"},
    {"name": "Masala Dosa", "calories": 340, "protein": 8, "carbs": 52, "fats": 11, "serving_size": "1 dosa", "category": "Indian Breakfast"},
    {"name": "Plain Dosa", "calories": 168, "protein": 4, "carbs": 30, "fats": 4, "serving_size": "1 dosa", "category": "Indian Breakfast"},
    {"name": "Uttapam", "calories": 197, "protein": 6, "carbs": 35, "fats": 4, "serving_size": "1 piece", "category": "Indian Breakfast"},
    {"name": "Upma", "calories": 230, "protein": 5, "carbs": 38, "fats": 7, "serving_size": "1 cup (200g)", "category": "Indian Breakfast"},
    {"name": "Poha (flattened rice)", "calories": 250, "protein": 5, "carbs": 45, "fats": 6, "serving_size": "1 cup (200g)", "category": "Indian Breakfast"},
    {"name": "Aloo Paratha", "calories": 300, "protein": 7, "carbs": 45, "fats": 11, "serving_size": "1 paratha", "category": "Indian Breakfast"},
    {"name": "Besan Chilla (chickpea pancake)", "calories": 180, "protein": 9, "carbs": 22, "fats": 6, "serving_size": "1 chilla", "category": "Indian Breakfast"},
    {"name": "Medu Vada", "calories": 175, "protein": 6, "carbs": 22, "fats": 8, "serving_size": "1 piece (60g)", "category": "Indian Breakfast"},
    {"name": "Rava Idli", "calories": 95, "protein": 3, "carbs": 16, "fats": 2.5, "serving_size": "1 piece (60g)", "category": "Indian Breakfast"},
    {"name": "Pongal", "calories": 220, "protein": 7, "carbs": 36, "fats": 6, "serving_size": "1 cup (200g)", "category": "Indian Breakfast"},
    {"name": "Paratha (plain)", "calories": 260, "protein": 6, "carbs": 40, "fats": 9, "serving_size": "1 paratha", "category": "Indian Breakfast"},

    # ── Indian Rice & Breads ───────────────────────────────────────────────────
    {"name": "Basmati Rice (cooked)", "calories": 200, "protein": 4.4, "carbs": 44, "fats": 0.4, "serving_size": "1 cup (180g)", "category": "Indian Grains"},
    {"name": "Jeera Rice", "calories": 220, "protein": 4.5, "carbs": 44, "fats": 4, "serving_size": "1 cup (200g)", "category": "Indian Grains"},
    {"name": "Roti / Chapati", "calories": 80, "protein": 3, "carbs": 15, "fats": 1.5, "serving_size": "1 roti (30g)", "category": "Indian Grains"},
    {"name": "Naan", "calories": 262, "protein": 9, "carbs": 45, "fats": 5, "serving_size": "1 piece (90g)", "category": "Indian Grains"},
    {"name": "Puri", "calories": 170, "protein": 3, "carbs": 22, "fats": 8, "serving_size": "2 pieces", "category": "Indian Grains"},
    {"name": "Bhatura", "calories": 300, "protein": 6, "carbs": 40, "fats": 13, "serving_size": "1 piece", "category": "Indian Grains"},
    {"name": "Biryani (chicken)", "calories": 490, "protein": 28, "carbs": 60, "fats": 14, "serving_size": "1 plate (350g)", "category": "Indian Grains"},
    {"name": "Biryani (vegetable)", "calories": 380, "protein": 9, "carbs": 65, "fats": 9, "serving_size": "1 plate (350g)", "category": "Indian Grains"},
    {"name": "Khichdi", "calories": 220, "protein": 8, "carbs": 38, "fats": 4, "serving_size": "1 cup (200g)", "category": "Indian Grains"},

    # ── Indian Dal & Lentils ───────────────────────────────────────────────────
    {"name": "Dal Tadka", "calories": 160, "protein": 9, "carbs": 22, "fats": 5, "serving_size": "1 cup (200g)", "category": "Indian Dal"},
    {"name": "Dal Makhani", "calories": 230, "protein": 11, "carbs": 28, "fats": 8, "serving_size": "1 cup (200g)", "category": "Indian Dal"},
    {"name": "Chana Masala", "calories": 270, "protein": 14, "carbs": 38, "fats": 7, "serving_size": "1 cup (200g)", "category": "Indian Dal"},
    {"name": "Rajma (kidney bean curry)", "calories": 260, "protein": 13, "carbs": 40, "fats": 5, "serving_size": "1 cup (200g)", "category": "Indian Dal"},
    {"name": "Moong Dal (yellow)", "calories": 140, "protein": 9, "carbs": 22, "fats": 1, "serving_size": "1 cup (200g)", "category": "Indian Dal"},
    {"name": "Sambhar", "calories": 120, "protein": 6, "carbs": 18, "fats": 3, "serving_size": "1 cup (200g)", "category": "Indian Dal"},
    {"name": "Chole (spiced chickpeas)", "calories": 270, "protein": 14, "carbs": 38, "fats": 7, "serving_size": "1 cup (200g)", "category": "Indian Dal"},

    # ── Indian Curries – Chicken ───────────────────────────────────────────────
    {"name": "Butter Chicken (Murgh Makhani)", "calories": 310, "protein": 28, "carbs": 10, "fats": 18, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Chicken Tikka Masala", "calories": 300, "protein": 26, "carbs": 12, "fats": 17, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Chicken Korma", "calories": 360, "protein": 27, "carbs": 14, "fats": 23, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Chicken Vindaloo", "calories": 280, "protein": 25, "carbs": 9, "fats": 16, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Saag Chicken (Palak Chicken)", "calories": 250, "protein": 26, "carbs": 8, "fats": 13, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Chicken Tikka", "calories": 220, "protein": 30, "carbs": 4, "fats": 9, "serving_size": "100g", "category": "Indian Curry"},
    {"name": "Kadai Chicken", "calories": 285, "protein": 27, "carbs": 10, "fats": 16, "serving_size": "1 cup (250g)", "category": "Indian Curry"},

    # ── Indian Curries – Mutton & Lamb ─────────────────────────────────────────
    {"name": "Mutton Curry", "calories": 330, "protein": 25, "carbs": 8, "fats": 22, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Mutton Rogan Josh", "calories": 340, "protein": 26, "carbs": 7, "fats": 24, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Keema (minced lamb)", "calories": 310, "protein": 24, "carbs": 5, "fats": 22, "serving_size": "100g", "category": "Indian Curry"},
    {"name": "Nihari (slow-cooked beef/lamb)", "calories": 380, "protein": 28, "carbs": 10, "fats": 26, "serving_size": "1 cup (250g)", "category": "Indian Curry"},

    # ── Indian Curries – Vegetarian ────────────────────────────────────────────
    {"name": "Paneer Butter Masala", "calories": 350, "protein": 16, "carbs": 15, "fats": 26, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Palak Paneer (spinach & cottage cheese)", "calories": 300, "protein": 15, "carbs": 12, "fats": 22, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Shahi Paneer", "calories": 380, "protein": 15, "carbs": 18, "fats": 29, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Matar Paneer", "calories": 280, "protein": 14, "carbs": 20, "fats": 17, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Aloo Gobi", "calories": 190, "protein": 5, "carbs": 28, "fats": 7, "serving_size": "1 cup (200g)", "category": "Indian Curry"},
    {"name": "Baingan Bharta (roasted eggplant)", "calories": 150, "protein": 4, "carbs": 20, "fats": 6, "serving_size": "1 cup (200g)", "category": "Indian Curry"},
    {"name": "Bhindi Masala (okra)", "calories": 140, "protein": 3, "carbs": 16, "fats": 7, "serving_size": "1 cup (200g)", "category": "Indian Curry"},
    {"name": "Saag (spinach curry)", "calories": 160, "protein": 7, "carbs": 12, "fats": 9, "serving_size": "1 cup (200g)", "category": "Indian Curry"},
    {"name": "Aloo Matar (potato & peas)", "calories": 210, "protein": 6, "carbs": 32, "fats": 7, "serving_size": "1 cup (200g)", "category": "Indian Curry"},
    {"name": "Mixed Vegetable Curry", "calories": 170, "protein": 5, "carbs": 22, "fats": 7, "serving_size": "1 cup (200g)", "category": "Indian Curry"},
    {"name": "Navratan Korma", "calories": 320, "protein": 9, "carbs": 28, "fats": 20, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Kadai Paneer", "calories": 340, "protein": 15, "carbs": 16, "fats": 25, "serving_size": "1 cup (250g)", "category": "Indian Curry"},
    {"name": "Methi Malai Paneer", "calories": 360, "protein": 15, "carbs": 14, "fats": 28, "serving_size": "1 cup (250g)", "category": "Indian Curry"},

    # ── Indian Seafood ─────────────────────────────────────────────────────────
    {"name": "Fish Curry (Goan)", "calories": 270, "protein": 24, "carbs": 8, "fats": 16, "serving_size": "1 cup (250g)", "category": "Indian Seafood"},
    {"name": "Prawn Masala", "calories": 240, "protein": 26, "carbs": 7, "fats": 12, "serving_size": "1 cup (200g)", "category": "Indian Seafood"},
    {"name": "Fish Tikka", "calories": 190, "protein": 28, "carbs": 4, "fats": 7, "serving_size": "100g", "category": "Indian Seafood"},
    {"name": "Koliwada Prawns (battered)", "calories": 320, "protein": 22, "carbs": 20, "fats": 16, "serving_size": "100g", "category": "Indian Seafood"},
    {"name": "Kerala Fish Curry", "calories": 260, "protein": 22, "carbs": 10, "fats": 15, "serving_size": "1 cup (250g)", "category": "Indian Seafood"},

    # ── Indian Snacks & Street Food ────────────────────────────────────────────
    {"name": "Samosa (vegetable)", "calories": 260, "protein": 5, "carbs": 35, "fats": 12, "serving_size": "2 pieces", "category": "Indian Snacks"},
    {"name": "Pakora (mixed vegetable)", "calories": 220, "protein": 5, "carbs": 26, "fats": 11, "serving_size": "5 pieces", "category": "Indian Snacks"},
    {"name": "Pani Puri / Gol Gappa", "calories": 180, "protein": 4, "carbs": 32, "fats": 5, "serving_size": "6 pieces", "category": "Indian Snacks"},
    {"name": "Bhel Puri", "calories": 180, "protein": 5, "carbs": 30, "fats": 5, "serving_size": "1 cup (150g)", "category": "Indian Snacks"},
    {"name": "Sev Puri", "calories": 210, "protein": 5, "carbs": 32, "fats": 8, "serving_size": "1 plate (5 pieces)", "category": "Indian Snacks"},
    {"name": "Pav Bhaji", "calories": 460, "protein": 12, "carbs": 68, "fats": 16, "serving_size": "1 plate (2 pav + bhaji)", "category": "Indian Snacks"},
    {"name": "Vada Pav", "calories": 290, "protein": 7, "carbs": 45, "fats": 9, "serving_size": "1 piece", "category": "Indian Snacks"},
    {"name": "Kachori", "calories": 250, "protein": 5, "carbs": 30, "fats": 13, "serving_size": "1 piece", "category": "Indian Snacks"},
    {"name": "Dhokla", "calories": 150, "protein": 7, "carbs": 25, "fats": 3, "serving_size": "4 pieces (150g)", "category": "Indian Snacks"},
    {"name": "Aloo Tikki", "calories": 200, "protein": 4, "carbs": 30, "fats": 7, "serving_size": "2 pieces", "category": "Indian Snacks"},
    {"name": "Dahi Puri", "calories": 200, "protein": 6, "carbs": 33, "fats": 5, "serving_size": "6 pieces", "category": "Indian Snacks"},
    {"name": "Papdi Chaat", "calories": 230, "protein": 7, "carbs": 35, "fats": 7, "serving_size": "1 plate (200g)", "category": "Indian Snacks"},
    {"name": "Chakli (rice flour spirals)", "calories": 490, "protein": 7, "carbs": 60, "fats": 25, "serving_size": "100g", "category": "Indian Snacks"},
    {"name": "Murukku", "calories": 510, "protein": 8, "carbs": 64, "fats": 24, "serving_size": "100g", "category": "Indian Snacks"},
    {"name": "Mixture (namkeen)", "calories": 480, "protein": 11, "carbs": 58, "fats": 23, "serving_size": "100g", "category": "Indian Snacks"},

    # ── Indian Dairy & Paneer ──────────────────────────────────────────────────
    {"name": "Paneer (cottage cheese)", "calories": 265, "protein": 18, "carbs": 3, "fats": 20, "serving_size": "100g", "category": "Indian Dairy"},
    {"name": "Dahi / Curd (plain)", "calories": 98, "protein": 11, "carbs": 8, "fats": 2, "serving_size": "1 cup (240g)", "category": "Indian Dairy"},
    {"name": "Lassi (sweet)", "calories": 260, "protein": 9, "carbs": 40, "fats": 6, "serving_size": "1 glass (300ml)", "category": "Indian Dairy"},
    {"name": "Lassi (salted)", "calories": 120, "protein": 8, "carbs": 14, "fats": 3, "serving_size": "1 glass (300ml)", "category": "Indian Dairy"},
    {"name": "Chaas / Buttermilk", "calories": 50, "protein": 4, "carbs": 5, "fats": 1, "serving_size": "1 glass (250ml)", "category": "Indian Dairy"},
    {"name": "Raita (cucumber)", "calories": 90, "protein": 5, "carbs": 9, "fats": 3, "serving_size": "1 cup (200g)", "category": "Indian Dairy"},
    {"name": "Shrikhand", "calories": 280, "protein": 8, "carbs": 42, "fats": 8, "serving_size": "100g", "category": "Indian Dairy"},
    {"name": "Ghee", "calories": 135, "protein": 0, "carbs": 0, "fats": 15, "serving_size": "1 tbsp (15g)", "category": "Indian Dairy"},

    # ── Indian Rice Dishes ─────────────────────────────────────────────────────
    {"name": "Curd Rice", "calories": 230, "protein": 7, "carbs": 38, "fats": 5, "serving_size": "1 cup (200g)", "category": "Indian Rice"},
    {"name": "Lemon Rice", "calories": 240, "protein": 5, "carbs": 44, "fats": 5, "serving_size": "1 cup (200g)", "category": "Indian Rice"},
    {"name": "Tamarind Rice (Puliyodarai)", "calories": 250, "protein": 4, "carbs": 46, "fats": 6, "serving_size": "1 cup (200g)", "category": "Indian Rice"},
    {"name": "Tomato Rice", "calories": 230, "protein": 4.5, "carbs": 43, "fats": 5, "serving_size": "1 cup (200g)", "category": "Indian Rice"},
    {"name": "Pulao (vegetable)", "calories": 290, "protein": 6, "carbs": 52, "fats": 7, "serving_size": "1 cup (220g)", "category": "Indian Rice"},
    {"name": "Egg Biryani", "calories": 420, "protein": 18, "carbs": 58, "fats": 13, "serving_size": "1 plate (350g)", "category": "Indian Rice"},

    # ── Indian Tandoor & Kebabs ────────────────────────────────────────────────
    {"name": "Tandoori Chicken", "calories": 185, "protein": 28, "carbs": 4, "fats": 6, "serving_size": "100g", "category": "Indian Tandoor"},
    {"name": "Seekh Kebab", "calories": 250, "protein": 22, "carbs": 6, "fats": 15, "serving_size": "2 skewers (100g)", "category": "Indian Tandoor"},
    {"name": "Shami Kebab", "calories": 200, "protein": 18, "carbs": 10, "fats": 10, "serving_size": "2 pieces (80g)", "category": "Indian Tandoor"},
    {"name": "Hariyali Kebab (green herb chicken)", "calories": 195, "protein": 27, "carbs": 5, "fats": 8, "serving_size": "100g", "category": "Indian Tandoor"},
    {"name": "Paneer Tikka", "calories": 270, "protein": 16, "carbs": 8, "fats": 19, "serving_size": "100g", "category": "Indian Tandoor"},
    {"name": "Tandoori Roti", "calories": 95, "protein": 3.5, "carbs": 18, "fats": 1.5, "serving_size": "1 roti (40g)", "category": "Indian Tandoor"},

    # ── Indian Sweets & Desserts ───────────────────────────────────────────────
    {"name": "Gulab Jamun", "calories": 175, "protein": 3, "carbs": 32, "fats": 5, "serving_size": "2 pieces (80g)", "category": "Indian Sweets"},
    {"name": "Rasgulla", "calories": 140, "protein": 4, "carbs": 30, "fats": 2, "serving_size": "2 pieces (80g)", "category": "Indian Sweets"},
    {"name": "Kheer (rice pudding)", "calories": 280, "protein": 8, "carbs": 46, "fats": 7, "serving_size": "1 cup (200g)", "category": "Indian Sweets"},
    {"name": "Halwa (sooji/semolina)", "calories": 370, "protein": 5, "carbs": 58, "fats": 13, "serving_size": "100g", "category": "Indian Sweets"},
    {"name": "Jalebi", "calories": 380, "protein": 3, "carbs": 75, "fats": 8, "serving_size": "100g", "category": "Indian Sweets"},
    {"name": "Barfi (milk fudge)", "calories": 370, "protein": 8, "carbs": 55, "fats": 14, "serving_size": "100g", "category": "Indian Sweets"},
    {"name": "Ladoo (besan)", "calories": 160, "protein": 3.5, "carbs": 22, "fats": 7, "serving_size": "1 piece (40g)", "category": "Indian Sweets"},
    {"name": "Payasam / Kheer (south Indian)", "calories": 260, "protein": 6, "carbs": 44, "fats": 7, "serving_size": "1 cup (200g)", "category": "Indian Sweets"},
    {"name": "Gajar Halwa (carrot pudding)", "calories": 260, "protein": 5, "carbs": 38, "fats": 10, "serving_size": "100g", "category": "Indian Sweets"},
    {"name": "Kaju Katli (cashew sweet)", "calories": 480, "protein": 10, "carbs": 60, "fats": 25, "serving_size": "100g", "category": "Indian Sweets"},

    # ── Indian Drinks ──────────────────────────────────────────────────────────
    {"name": "Masala Chai (with milk & sugar)", "calories": 90, "protein": 3, "carbs": 14, "fats": 2.5, "serving_size": "1 cup (200ml)", "category": "Indian Drinks"},
    {"name": "Masala Chai (no sugar)", "calories": 45, "protein": 2.5, "carbs": 5, "fats": 2, "serving_size": "1 cup (200ml)", "category": "Indian Drinks"},
    {"name": "Mango Lassi", "calories": 290, "protein": 8, "carbs": 50, "fats": 6, "serving_size": "1 glass (300ml)", "category": "Indian Drinks"},
    {"name": "Aam Panna (raw mango drink)", "calories": 90, "protein": 0.5, "carbs": 23, "fats": 0, "serving_size": "1 glass (250ml)", "category": "Indian Drinks"},
    {"name": "Rose Milk", "calories": 200, "protein": 6, "carbs": 34, "fats": 4, "serving_size": "1 glass (250ml)", "category": "Indian Drinks"},

    # ── South Indian Specials ──────────────────────────────────────────────────
    {"name": "Appam (Kerala rice pancake)", "calories": 120, "protein": 3, "carbs": 24, "fats": 1.5, "serving_size": "2 pieces", "category": "South Indian"},
    {"name": "Pesarattu (green moong dosa)", "calories": 155, "protein": 9, "carbs": 24, "fats": 3, "serving_size": "1 dosa", "category": "South Indian"},
    {"name": "Rasam", "calories": 60, "protein": 2, "carbs": 10, "fats": 2, "serving_size": "1 cup (200ml)", "category": "South Indian"},
    {"name": "Kootu (mixed vegetable & lentil)", "calories": 170, "protein": 7, "carbs": 24, "fats": 5, "serving_size": "1 cup (200g)", "category": "South Indian"},
    {"name": "Avial (mixed vegetables in coconut)", "calories": 180, "protein": 5, "carbs": 18, "fats": 10, "serving_size": "1 cup (200g)", "category": "South Indian"},
    {"name": "Puttu (steamed rice cake with coconut)", "calories": 220, "protein": 5, "carbs": 42, "fats": 4, "serving_size": "1 serving (150g)", "category": "South Indian"},
    {"name": "Idiyappam (string hoppers)", "calories": 130, "protein": 2, "carbs": 28, "fats": 0.5, "serving_size": "3 pieces", "category": "South Indian"},

    # ── North Indian Specials ──────────────────────────────────────────────────
    {"name": "Chole Bhature", "calories": 580, "protein": 18, "carbs": 78, "fats": 22, "serving_size": "1 plate (2 bhature + chole)", "category": "North Indian"},
    {"name": "Dal Baati Churma", "calories": 620, "protein": 16, "carbs": 82, "fats": 26, "serving_size": "1 plate", "category": "North Indian"},
    {"name": "Litti Chokha", "calories": 450, "protein": 13, "carbs": 64, "fats": 16, "serving_size": "3 pieces + chokha", "category": "North Indian"},
    {"name": "Kadhi Pakoda", "calories": 250, "protein": 9, "carbs": 28, "fats": 11, "serving_size": "1 cup (200g)", "category": "North Indian"},
    {"name": "Sarson Da Saag", "calories": 200, "protein": 9, "carbs": 20, "fats": 9, "serving_size": "1 cup (200g)", "category": "North Indian"},
    {"name": "Makki Di Roti", "calories": 170, "protein": 4, "carbs": 32, "fats": 4, "serving_size": "1 roti (60g)", "category": "North Indian"},
    {"name": "Stuffed Paratha (mixed)", "calories": 320, "protein": 8, "carbs": 48, "fats": 12, "serving_size": "1 paratha", "category": "North Indian"},

    # Additional global breakfast
    {"name": "Pancakes", "calories": 227, "protein": 6, "carbs": 28, "fats": 10, "serving_size": "2 pancakes", "category": "Breakfast"},
    {"name": "French Toast", "calories": 250, "protein": 9, "carbs": 27, "fats": 11, "serving_size": "2 slices", "category": "Breakfast"},
    {"name": "Bagel", "calories": 245, "protein": 10, "carbs": 48, "fats": 1.5, "serving_size": "1 bagel", "category": "Breakfast"},
    {"name": "Croissant", "calories": 231, "protein": 5, "carbs": 26, "fats": 12, "serving_size": "1 piece", "category": "Breakfast"},
    {"name": "Waffles", "calories": 218, "protein": 6, "carbs": 25, "fats": 10, "serving_size": "2 waffles", "category": "Breakfast"},
    {"name": "Breakfast Burrito", "calories": 320, "protein": 18, "carbs": 28, "fats": 15, "serving_size": "1 burrito", "category": "Breakfast"},
    {"name": "Egg White Omelette", "calories": 120, "protein": 20, "carbs": 3, "fats": 3, "serving_size": "1 omelette", "category": "Breakfast"},
    {"name": "Hash Browns", "calories": 143, "protein": 2, "carbs": 15, "fats": 9, "serving_size": "1 patty", "category": "Breakfast"},
    {"name": "Granola", "calories": 220, "protein": 5, "carbs": 32, "fats": 8, "serving_size": "1/2 cup", "category": "Breakfast"},
    {"name": "Muesli", "calories": 190, "protein": 6, "carbs": 33, "fats": 4, "serving_size": "1/2 cup dry", "category": "Breakfast"},

    # Additional proteins and seafood
    {"name": "Chicken Thigh (roasted)", "calories": 209, "protein": 26, "carbs": 0, "fats": 11, "serving_size": "100g", "category": "Protein"},
    {"name": "Pork Chop", "calories": 231, "protein": 25, "carbs": 0, "fats": 14, "serving_size": "100g", "category": "Protein"},
    {"name": "Tofu", "calories": 144, "protein": 17, "carbs": 3, "fats": 8, "serving_size": "100g", "category": "Protein"},
    {"name": "Tempeh", "calories": 193, "protein": 20, "carbs": 9, "fats": 11, "serving_size": "100g", "category": "Protein"},
    {"name": "Shrimp (boiled)", "calories": 99, "protein": 24, "carbs": 0.2, "fats": 0.3, "serving_size": "100g", "category": "Protein"},
    {"name": "Sardines", "calories": 208, "protein": 25, "carbs": 0, "fats": 11, "serving_size": "100g", "category": "Protein"},
    {"name": "Prawns (grilled)", "calories": 110, "protein": 23, "carbs": 1, "fats": 1.5, "serving_size": "100g", "category": "Protein"},
    {"name": "Paneer Bhurji", "calories": 265, "protein": 16, "carbs": 8, "fats": 18, "serving_size": "1 cup", "category": "Protein"},

    # More grains and staples
    {"name": "White Rice", "calories": 205, "protein": 4.3, "carbs": 45, "fats": 0.4, "serving_size": "1 cup cooked", "category": "Grains"},
    {"name": "Couscous", "calories": 176, "protein": 6, "carbs": 36, "fats": 0.3, "serving_size": "1 cup cooked", "category": "Grains"},
    {"name": "Barley", "calories": 193, "protein": 3.5, "carbs": 44, "fats": 0.7, "serving_size": "1 cup cooked", "category": "Grains"},
    {"name": "Millet", "calories": 207, "protein": 6, "carbs": 41, "fats": 1.7, "serving_size": "1 cup cooked", "category": "Grains"},
    {"name": "Corn Tortilla", "calories": 104, "protein": 3, "carbs": 22, "fats": 1.5, "serving_size": "2 tortillas", "category": "Grains"},
    {"name": "Flour Tortilla", "calories": 144, "protein": 4, "carbs": 24, "fats": 4, "serving_size": "1 tortilla", "category": "Grains"},
    {"name": "Baguette", "calories": 180, "protein": 6, "carbs": 36, "fats": 1, "serving_size": "75g", "category": "Grains"},
    {"name": "Pita Bread", "calories": 170, "protein": 6, "carbs": 35, "fats": 1, "serving_size": "1 pita", "category": "Grains"},

    # More vegetables
    {"name": "Carrots", "calories": 50, "protein": 1, "carbs": 12, "fats": 0.3, "serving_size": "1 cup chopped", "category": "Vegetables"},
    {"name": "Cauliflower", "calories": 27, "protein": 2, "carbs": 5, "fats": 0.3, "serving_size": "1 cup", "category": "Vegetables"},
    {"name": "Green Beans", "calories": 44, "protein": 2.4, "carbs": 10, "fats": 0.3, "serving_size": "1 cup", "category": "Vegetables"},
    {"name": "Cucumber", "calories": 16, "protein": 0.7, "carbs": 4, "fats": 0.1, "serving_size": "1 cup sliced", "category": "Vegetables"},
    {"name": "Zucchini", "calories": 27, "protein": 2, "carbs": 5, "fats": 0.4, "serving_size": "1 cup", "category": "Vegetables"},
    {"name": "Mushrooms", "calories": 22, "protein": 3, "carbs": 3, "fats": 0.3, "serving_size": "100g", "category": "Vegetables"},
    {"name": "Asparagus", "calories": 27, "protein": 3, "carbs": 5, "fats": 0.2, "serving_size": "1 cup", "category": "Vegetables"},
    {"name": "Cabbage", "calories": 22, "protein": 1.1, "carbs": 5, "fats": 0.1, "serving_size": "1 cup shredded", "category": "Vegetables"},

    # More fruits
    {"name": "Mango", "calories": 99, "protein": 1.4, "carbs": 25, "fats": 0.6, "serving_size": "1 cup sliced", "category": "Fruit"},
    {"name": "Pineapple", "calories": 82, "protein": 0.9, "carbs": 22, "fats": 0.2, "serving_size": "1 cup", "category": "Fruit"},
    {"name": "Watermelon", "calories": 46, "protein": 0.9, "carbs": 11, "fats": 0.2, "serving_size": "1 cup", "category": "Fruit"},
    {"name": "Grapes", "calories": 104, "protein": 1.1, "carbs": 27, "fats": 0.2, "serving_size": "1 cup", "category": "Fruit"},
    {"name": "Pear", "calories": 101, "protein": 0.6, "carbs": 27, "fats": 0.3, "serving_size": "1 medium", "category": "Fruit"},
    {"name": "Kiwi", "calories": 42, "protein": 0.8, "carbs": 10, "fats": 0.4, "serving_size": "1 medium", "category": "Fruit"},
    {"name": "Papaya", "calories": 55, "protein": 0.9, "carbs": 14, "fats": 0.2, "serving_size": "1 cup", "category": "Fruit"},
    {"name": "Guava", "calories": 112, "protein": 4.2, "carbs": 24, "fats": 1.6, "serving_size": "1 cup", "category": "Fruit"},
    {"name": "Pomegranate", "calories": 144, "protein": 3, "carbs": 32, "fats": 2, "serving_size": "1 cup arils", "category": "Fruit"},

    # More dairy
    {"name": "Low-Fat Milk", "calories": 102, "protein": 8, "carbs": 12, "fats": 2.4, "serving_size": "1 cup", "category": "Dairy"},
    {"name": "Skim Milk", "calories": 83, "protein": 8, "carbs": 12, "fats": 0.2, "serving_size": "1 cup", "category": "Dairy"},
    {"name": "Mozzarella Cheese", "calories": 85, "protein": 6, "carbs": 1, "fats": 6, "serving_size": "28g / 1 oz", "category": "Dairy"},
    {"name": "Parmesan Cheese", "calories": 111, "protein": 10, "carbs": 1, "fats": 7, "serving_size": "28g / 1 oz", "category": "Dairy"},
    {"name": "Vanilla Yogurt", "calories": 150, "protein": 6, "carbs": 24, "fats": 3, "serving_size": "1 cup", "category": "Dairy"},
    {"name": "Chocolate Milk", "calories": 190, "protein": 8, "carbs": 26, "fats": 5, "serving_size": "1 cup", "category": "Dairy"},

    # More legumes and nuts
    {"name": "Chickpeas", "calories": 269, "protein": 14.5, "carbs": 45, "fats": 4.2, "serving_size": "1 cup cooked", "category": "Legumes"},
    {"name": "Kidney Beans", "calories": 225, "protein": 15, "carbs": 40, "fats": 0.9, "serving_size": "1 cup cooked", "category": "Legumes"},
    {"name": "Edamame", "calories": 188, "protein": 18, "carbs": 14, "fats": 8, "serving_size": "1 cup", "category": "Legumes"},
    {"name": "Green Peas", "calories": 134, "protein": 8.5, "carbs": 25, "fats": 0.4, "serving_size": "1 cup", "category": "Legumes"},
    {"name": "Cashews", "calories": 157, "protein": 5, "carbs": 9, "fats": 12, "serving_size": "28g / 1 oz", "category": "Nuts"},
    {"name": "Walnuts", "calories": 185, "protein": 4.3, "carbs": 4, "fats": 18.5, "serving_size": "28g / 1 oz", "category": "Nuts"},
    {"name": "Pistachios", "calories": 159, "protein": 6, "carbs": 8, "fats": 13, "serving_size": "28g / 1 oz", "category": "Nuts"},
    {"name": "Trail Mix", "calories": 173, "protein": 4, "carbs": 15, "fats": 11, "serving_size": "1/4 cup", "category": "Nuts"},

    # Salads and soups
    {"name": "Caesar Salad", "calories": 180, "protein": 7, "carbs": 8, "fats": 14, "serving_size": "1 bowl", "category": "Salads"},
    {"name": "Greek Salad", "calories": 211, "protein": 6, "carbs": 13, "fats": 15, "serving_size": "1 bowl", "category": "Salads"},
    {"name": "Chicken Salad", "calories": 260, "protein": 24, "carbs": 9, "fats": 14, "serving_size": "1 bowl", "category": "Salads"},
    {"name": "Cobb Salad", "calories": 320, "protein": 21, "carbs": 10, "fats": 21, "serving_size": "1 bowl", "category": "Salads"},
    {"name": "Tomato Soup", "calories": 90, "protein": 2, "carbs": 18, "fats": 1.5, "serving_size": "1 cup", "category": "Soups"},
    {"name": "Chicken Noodle Soup", "calories": 120, "protein": 7, "carbs": 14, "fats": 4, "serving_size": "1 cup", "category": "Soups"},
    {"name": "Minestrone Soup", "calories": 110, "protein": 5, "carbs": 19, "fats": 2.5, "serving_size": "1 cup", "category": "Soups"},
    {"name": "Hot and Sour Soup", "calories": 95, "protein": 4, "carbs": 12, "fats": 3, "serving_size": "1 cup", "category": "Soups"},

    # Fast food and mains
    {"name": "Cheeseburger", "calories": 303, "protein": 17, "carbs": 30, "fats": 14, "serving_size": "1 burger", "category": "Fast Food"},
    {"name": "Veggie Burger", "calories": 250, "protein": 12, "carbs": 31, "fats": 9, "serving_size": "1 burger", "category": "Fast Food"},
    {"name": "French Fries", "calories": 365, "protein": 4, "carbs": 48, "fats": 17, "serving_size": "1 medium serving", "category": "Fast Food"},
    {"name": "Pizza Slice (cheese)", "calories": 285, "protein": 12, "carbs": 36, "fats": 10, "serving_size": "1 slice", "category": "Fast Food"},
    {"name": "Pizza Slice (pepperoni)", "calories": 313, "protein": 13, "carbs": 35, "fats": 13, "serving_size": "1 slice", "category": "Fast Food"},
    {"name": "Chicken Sandwich", "calories": 360, "protein": 24, "carbs": 32, "fats": 15, "serving_size": "1 sandwich", "category": "Fast Food"},
    {"name": "Falafel Wrap", "calories": 330, "protein": 11, "carbs": 39, "fats": 14, "serving_size": "1 wrap", "category": "Fast Food"},
    {"name": "Chicken Shawarma Wrap", "calories": 390, "protein": 24, "carbs": 33, "fats": 18, "serving_size": "1 wrap", "category": "Fast Food"},
    {"name": "Tacos (beef)", "calories": 250, "protein": 13, "carbs": 20, "fats": 13, "serving_size": "2 tacos", "category": "Fast Food"},
    {"name": "Burrito Bowl", "calories": 520, "protein": 28, "carbs": 54, "fats": 20, "serving_size": "1 bowl", "category": "Fast Food"},

    # Pasta and noodle dishes
    {"name": "Mac and Cheese", "calories": 310, "protein": 10, "carbs": 36, "fats": 14, "serving_size": "1 cup", "category": "Pasta"},
    {"name": "Spaghetti Bolognese", "calories": 390, "protein": 20, "carbs": 48, "fats": 12, "serving_size": "1 plate", "category": "Pasta"},
    {"name": "Fettuccine Alfredo", "calories": 415, "protein": 14, "carbs": 42, "fats": 21, "serving_size": "1 plate", "category": "Pasta"},
    {"name": "Lasagna", "calories": 336, "protein": 19, "carbs": 30, "fats": 16, "serving_size": "1 slice", "category": "Pasta"},
    {"name": "Vegetable Chow Mein", "calories": 310, "protein": 8, "carbs": 49, "fats": 9, "serving_size": "1 plate", "category": "Noodles"},
    {"name": "Chicken Hakka Noodles", "calories": 360, "protein": 18, "carbs": 46, "fats": 11, "serving_size": "1 plate", "category": "Noodles"},
    {"name": "Pad Thai", "calories": 357, "protein": 13, "carbs": 45, "fats": 14, "serving_size": "1 plate", "category": "Noodles"},
    {"name": "Ramen", "calories": 430, "protein": 15, "carbs": 53, "fats": 17, "serving_size": "1 bowl", "category": "Noodles"},

    # Desserts and bakery
    {"name": "Chocolate Cake", "calories": 352, "protein": 5, "carbs": 50, "fats": 15, "serving_size": "1 slice", "category": "Desserts"},
    {"name": "Cheesecake", "calories": 321, "protein": 6, "carbs": 25, "fats": 22, "serving_size": "1 slice", "category": "Desserts"},
    {"name": "Brownie", "calories": 243, "protein": 3, "carbs": 33, "fats": 11, "serving_size": "1 piece", "category": "Desserts"},
    {"name": "Ice Cream (vanilla)", "calories": 137, "protein": 2.3, "carbs": 16, "fats": 7, "serving_size": "1/2 cup", "category": "Desserts"},
    {"name": "Donut", "calories": 260, "protein": 4, "carbs": 31, "fats": 14, "serving_size": "1 donut", "category": "Desserts"},
    {"name": "Chocolate Chip Cookie", "calories": 160, "protein": 2, "carbs": 22, "fats": 7, "serving_size": "1 large cookie", "category": "Desserts"},
    {"name": "Banana Bread", "calories": 196, "protein": 3, "carbs": 33, "fats": 6, "serving_size": "1 slice", "category": "Desserts"},

    # Beverage expansion
    {"name": "Black Coffee", "calories": 2, "protein": 0.3, "carbs": 0, "fats": 0, "serving_size": "1 cup (240ml)", "category": "Beverages"},
    {"name": "Cappuccino", "calories": 80, "protein": 4, "carbs": 8, "fats": 3, "serving_size": "1 cup (240ml)", "category": "Beverages"},
    {"name": "Latte", "calories": 120, "protein": 6, "carbs": 12, "fats": 4, "serving_size": "1 cup (240ml)", "category": "Beverages"},
    {"name": "Iced Coffee", "calories": 90, "protein": 2, "carbs": 15, "fats": 2, "serving_size": "1 glass (300ml)", "category": "Beverages"},
    {"name": "Green Tea", "calories": 2, "protein": 0, "carbs": 0, "fats": 0, "serving_size": "1 cup (240ml)", "category": "Beverages"},
    {"name": "Lemonade", "calories": 99, "protein": 0, "carbs": 25, "fats": 0, "serving_size": "1 glass (250ml)", "category": "Beverages"},
    {"name": "Orange Juice", "calories": 112, "protein": 1.7, "carbs": 26, "fats": 0.5, "serving_size": "1 glass (240ml)", "category": "Beverages"},
    {"name": "Apple Juice", "calories": 114, "protein": 0.2, "carbs": 28, "fats": 0.3, "serving_size": "1 glass (240ml)", "category": "Beverages"},
    {"name": "Coconut Water", "calories": 46, "protein": 1.7, "carbs": 9, "fats": 0.5, "serving_size": "1 glass (240ml)", "category": "Beverages"},
    {"name": "Cola", "calories": 140, "protein": 0, "carbs": 39, "fats": 0, "serving_size": "1 can (330ml)", "category": "Beverages"},
    {"name": "Diet Cola", "calories": 1, "protein": 0, "carbs": 0, "fats": 0, "serving_size": "1 can (330ml)", "category": "Beverages"},
    {"name": "Chocolate Milkshake", "calories": 380, "protein": 9, "carbs": 52, "fats": 15, "serving_size": "1 glass (350ml)", "category": "Beverages"},
    {"name": "Strawberry Smoothie", "calories": 180, "protein": 5, "carbs": 35, "fats": 2, "serving_size": "1 glass (300ml)", "category": "Beverages"},
    {"name": "Protein Shake", "calories": 160, "protein": 24, "carbs": 8, "fats": 3, "serving_size": "1 shake", "category": "Beverages"},

    # More Indian foods
    {"name": "Misal Pav", "calories": 420, "protein": 14, "carbs": 58, "fats": 15, "serving_size": "1 plate", "category": "Indian Snacks"},
    {"name": "Sabudana Khichdi", "calories": 320, "protein": 5, "carbs": 52, "fats": 10, "serving_size": "1 cup", "category": "Indian Breakfast"},
    {"name": "Thepla", "calories": 130, "protein": 3.5, "carbs": 18, "fats": 5, "serving_size": "1 piece", "category": "Indian Breakfast"},
    {"name": "Handvo", "calories": 210, "protein": 8, "carbs": 28, "fats": 7, "serving_size": "1 slice", "category": "Indian Snacks"},
    {"name": "Undhiyu", "calories": 240, "protein": 7, "carbs": 24, "fats": 12, "serving_size": "1 cup", "category": "Indian Curry"},
    {"name": "Kolhapuri Chicken", "calories": 295, "protein": 27, "carbs": 8, "fats": 17, "serving_size": "1 cup", "category": "Indian Curry"},
    {"name": "Egg Curry", "calories": 220, "protein": 12, "carbs": 8, "fats": 15, "serving_size": "1 cup", "category": "Indian Curry"},
    {"name": "Malai Kofta", "calories": 360, "protein": 10, "carbs": 26, "fats": 24, "serving_size": "1 cup", "category": "Indian Curry"},
    {"name": "Kofta Curry", "calories": 300, "protein": 12, "carbs": 22, "fats": 18, "serving_size": "1 cup", "category": "Indian Curry"},
    {"name": "Amritsari Kulcha", "calories": 310, "protein": 9, "carbs": 48, "fats": 9, "serving_size": "1 kulcha", "category": "North Indian"},
    {"name": "Kulfi", "calories": 180, "protein": 4, "carbs": 22, "fats": 8, "serving_size": "1 stick", "category": "Indian Sweets"},
    {"name": "Rabri", "calories": 260, "protein": 7, "carbs": 28, "fats": 13, "serving_size": "1/2 cup", "category": "Indian Sweets"},
    {"name": "Thandai", "calories": 210, "protein": 6, "carbs": 24, "fats": 10, "serving_size": "1 glass (250ml)", "category": "Indian Drinks"},
    {"name": "Sugarcane Juice", "calories": 180, "protein": 0, "carbs": 45, "fats": 0, "serving_size": "1 glass (300ml)", "category": "Indian Drinks"},
    {"name": "Filter Coffee", "calories": 85, "protein": 3, "carbs": 11, "fats": 3, "serving_size": "1 tumbler (180ml)", "category": "Indian Drinks"},
]


class Command(BaseCommand):
    help = "Seed the database with sample meal items including extensive Indian food"

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for meal_data in SAMPLE_MEALS:
            meal, created = Meal.objects.get_or_create(
                name=meal_data["name"],
                defaults=meal_data,
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete: {created_count} meals created, {skipped_count} already existed."
            )
        )
