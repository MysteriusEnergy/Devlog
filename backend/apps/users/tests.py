from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


class AuthAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.refresh_url = reverse("token_refresh")
        self.logout_url = reverse("logout")


    def test_user_can_register(self):
        response = self.client.post(self.register_url, {
            "email": "user@example.com",
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data["email"], "user@example.com")
        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertNotIn("password", response.data)


    def test_register_without_email_returns_400(self):
        response = self.client.post(self.register_url, {
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


    def test_user_can_login(self):
        User.objects.create_user(
            email="user@example.com",
            password="testpass123"
        )

        response = self.client.post(self.login_url, {
            "email": "user@example.com",
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertIn("expires_in", response.data)


    def test_login_with_invalid_credentials_returns_401(self):
        User.objects.create_user(
            email="user@example.com",
            password="testpass123"
        )

        response = self.client.post(self.login_url, {
            "email": "user@example.com",
            "password": "wrongpass"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["status"], status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Unauthorized")


    def test_refresh_token_returns_new_access_token(self):
        user = User.objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        refresh = RefreshToken.for_user(user)

        response = self.client.post(self.refresh_url, {
            "refresh_token": str(refresh)
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("expires_in", response.data)


    def test_logout_blacklists_refresh_token(self):
        user = User.objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        refresh = RefreshToken.for_user(user)

        logout_response = self.client.post(self.logout_url, {
            "refresh_token": str(refresh)
        })

        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)

        refresh_response = self.client.post(self.refresh_url, {
            "refresh_token": str(refresh)
        })

        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)