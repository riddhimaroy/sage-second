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
