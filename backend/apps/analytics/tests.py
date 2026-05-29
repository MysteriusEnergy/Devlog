from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.projects.models import Project
from apps.sessions.models import WorkSession
from apps.users.models import User


class AnalyticsSummaryAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="testpass123"
        )
        self.project = Project.objects.create(
            user=self.user, name="DevLog", color="#3B82F6"
        )
        self.other_project = Project.objects.create(
            user=self.user, name="Otro proyecto", color="#EF4444"
        )
        self.foreign_project = Project.objects.create(
            user=self.other_user, name="Proyecto ajeno", color="#10B981"
        )
        self.url = reverse("analytics-summary")
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_can_get_summary(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_minutes", response.data)
        self.assertIn("total_hours", response.data)
        self.assertIn("weekly_minutes", response.data)
        self.assertIn("project_breakdown", response.data)

    def test_unauthenticated_user_cannot_get_summary(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_total_minutes_only_includes_authenticated_user_sessions(self):
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-25",
            start_time="09:00",
            end_time="11:00",
            duration_minutes=120,
        )
        WorkSession.objects.create(
            user=self.other_user,
            project=self.foreign_project,
            date="2026-05-25",
            start_time="09:00",
            end_time="13:00",
            duration_minutes=240,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_minutes"], 120)
        self.assertEqual(response.data["total_hours"], 2.0)

    def test_project_breakdown_groups_minutes_by_project(self):
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-25",
            start_time="09:00",
            end_time="10:00",
            duration_minutes=60,
        )
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-26",
            start_time="10:00",
            end_time="11:00",
            duration_minutes=60,
        )
        WorkSession.objects.create(
            user=self.user,
            project=self.other_project,
            date="2026-05-27",
            start_time="11:00",
            end_time="12:30",
            duration_minutes=90,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        breakdown = {
            item["project_id"]: item["total_minutes"]
            for item in response.data["project_breakdown"]
        }

        self.assertEqual(breakdown[str(self.project.id)], 120)
        self.assertEqual(breakdown[str(self.other_project.id)], 90)

    def test_summary_can_be_filtered_by_date_range(self):
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-01",
            start_time="09:00",
            end_time="10:00",
            duration_minutes=60,
        )
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-20",
            start_time="09:00",
            end_time="11:00",
            duration_minutes=120,
        )

        response = self.client.get(f"{self.url}?from=2026-05-15&to=2026-05-31")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_minutes"], 120)

    def test_weekly_minutes_uses_current_week(self):
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())
        outside_week = week_start - timedelta(days=1)

        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date=week_start,
            start_time="09:00",
            end_time="10:00",
            duration_minutes=60,
        )
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date=outside_week,
            start_time="09:00",
            end_time="11:00",
            duration_minutes=120,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["weekly_minutes"], 60)

    def test_weekly_minutes_ignores_from_to_filters(self):
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())

        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date=week_start,
            start_time="09:00",
            end_time="10:00",
            duration_minutes=60,
        )
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-01",
            start_time="09:00",
            end_time="11:00",
            duration_minutes=120,
        )
        response = self.client.get(f"{self.url}?from=2026-05-01&to=2026-05-01")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_minutes"], 120)
        self.assertEqual(response.data["weekly_minutes"], 60)
