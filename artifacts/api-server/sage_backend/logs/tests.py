from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory

from meals.models import Meal
from .models import DailyLog, LogEntry
from .serializers import DailyLogSerializer


class DailyLogUserIsolationTests(TestCase):
    def setUp(self):
        self.user_one = User.objects.create_user(username="alice", password="pass1234")
        self.user_two = User.objects.create_user(username="bob", password="pass1234")
        self.meal = Meal.objects.create(
            name="Test Meal",
            calories=100,
            protein=10,
            carbs=20,
            fats=5,
            serving_size="1 bowl",
            category="Test",
        )

    def test_today_log_endpoint_returns_only_current_users_entries(self):
        DailyLog.objects.create(user=self.user_one, date="2026-04-08")
        DailyLog.objects.create(user=self.user_two, date="2026-04-08")

        client = APIClient()
        token_one = Token.objects.create(user=self.user_one)
        token_two = Token.objects.create(user=self.user_two)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_one.key}")
        add_response = client.post(
            "/api/logs/add",
            {"mealId": self.meal.id, "quantity": 2},
            format="json",
        )
        self.assertEqual(add_response.status_code, 201)

        client.credentials(HTTP_AUTHORIZATION=f"Token {token_two.key}")
        response = client.get("/api/logs/today")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["entries"], [])
        self.assertEqual(response.data["totals"]["calories"], 0.0)

    def test_serializer_scopes_entries_to_daily_log_owner_without_request_context(self):
        owner_log = DailyLog.objects.create(user=self.user_one, date="2026-04-08")
        LogEntry.objects.create(user=self.user_one, meal=self.meal, daily_log=owner_log, quantity=1)
        LogEntry.objects.create(user=self.user_two, meal=self.meal, daily_log=owner_log, quantity=3)

        data = DailyLogSerializer(owner_log).data

        self.assertEqual(len(data["entries"]), 1)
        self.assertEqual(data["entries"][0]["quantity"], 1.0)
        self.assertEqual(data["totals"]["calories"], 100.0)

    def test_serializer_scopes_entries_to_authenticated_request_user(self):
        owner_log = DailyLog.objects.create(user=self.user_one, date="2026-04-08")
        LogEntry.objects.create(user=self.user_one, meal=self.meal, daily_log=owner_log, quantity=1)

        factory = APIRequestFactory()
        request = factory.get("/api/logs/today")
        request.user = self.user_two

        data = DailyLogSerializer(owner_log, context={"request": request}).data

        self.assertEqual(data["entries"], [])
        self.assertEqual(data["totals"]["calories"], 0.0)

    def test_today_log_requires_authentication(self):
        client = APIClient()

        response = client.get("/api/logs/today")

        self.assertEqual(response.status_code, 401)

    def test_add_log_entry_rejects_fractional_quantity(self):
        client = APIClient()
        token = Token.objects.create(user=self.user_one)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = client.post(
            "/api/logs/add",
            {"mealId": self.meal.id, "quantity": 1.5},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "quantity must be a positive integer")

    def test_update_log_entry_rejects_fractional_quantity(self):
        client = APIClient()
        token = Token.objects.create(user=self.user_one)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        daily_log = DailyLog.objects.create(user=self.user_one, date="2026-04-08")
        entry = LogEntry.objects.create(user=self.user_one, meal=self.meal, daily_log=daily_log, quantity=1)

        response = client.patch(
            f"/api/logs/update/{entry.id}",
            {"quantity": 2.5},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "quantity must be a positive integer")
