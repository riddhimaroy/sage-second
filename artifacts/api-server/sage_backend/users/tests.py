from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserCrudTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="crud_user", password="pass1234")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_is_supported_via_register(self):
        response = self.client.post(
            "/api/auth/register",
            {"username": "crud_created", "password": "pass1234"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="crud_created").exists())

    def test_read_profile_returns_current_user(self):
        response = self.client.get("/api/auth/profile")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "crud_user")
        self.assertFalse(response.data["profileComplete"])

    def test_put_fully_updates_profile(self):
        response = self.client.put(
            "/api/auth/profile",
            {
                "age": 28,
                "gender": "female",
                "height_cm": 165,
                "weight_kg": 58,
                "activity_level": "moderate",
                "goal": "maintain",
                "custom_protein_g": None,
                "use_custom_protein": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["profileComplete"])
        self.assertEqual(response.data["age"], 28)
        self.assertEqual(response.data["activity_level"], "moderate")

    def test_patch_partially_updates_profile(self):
        response = self.client.patch(
            "/api/auth/profile",
            {"weight_kg": 72.5},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["weight_kg"], 72.5)

    def test_delete_removes_current_user(self):
        response = self.client.delete("/api/auth/profile")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="crud_user").exists())

    def test_change_password_updates_credentials_and_returns_new_token(self):
        response = self.client.post(
            "/api/auth/change-password",
            {"current_password": "pass1234", "new_password": "newpass567"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["token"])
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass567"))
