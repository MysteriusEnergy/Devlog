from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.projects.models import Project
from apps.sessions.models import WorkSession
from apps.users.models import User


class WorkSessionAPITests(APITestCase):
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
            user=self.other_user, name="Proyecto ajeno", color="#EF4444"
        )
        self.work_sessions_url = reverse("work-session-list")
        self.client.force_authenticate(user=self.user)

    def work_session_detail_url(self, work_session):
        return reverse("work-session-detail", kwargs={"pk": work_session.id})

    def test_authenticated_user_can_create_work_session(self):
        response = self.client.post(
            self.work_sessions_url,
            {
                "project_id": str(self.project.id),
                "date": "2026-05-25",
                "start_time": "09:00",
                "end_time": "11:00",
                "notes": "Trabajo en backend",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkSession.objects.count(), 1)
        self.assertEqual(WorkSession.objects.first().user, self.user)
        self.assertEqual(response.data["project_id"], str(self.project.id))

    def test_duration_minutes_is_calculated_automatically(self):
        response = self.client.post(
            self.work_sessions_url,
            {
                "project_id": str(self.project.id),
                "date": "2026-05-25",
                "start_time": "09:00",
                "end_time": "11:30",
                "notes": "Trabajo en backend",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["duration_minutes"], 150)
        self.assertEqual(WorkSession.objects.first().duration_minutes, 150)

    def test_unauthenticated_user_cannot_create_work_session(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.work_sessions_url,
            {
                "project_id": str(self.project.id),
                "date": "2026-05-25",
                "start_time": "09:00",
                "end_time": "11:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_create_work_session_with_other_user_project(self):
        response = self.client.post(
            self.work_sessions_url,
            {
                "project_id": str(self.other_project.id),
                "date": "2026-05-25",
                "start_time": "09:00",
                "end_time": "11:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("project_id", response.data)

    def test_start_time_must_be_before_end_time(self):
        response = self.client.post(
            self.work_sessions_url,
            {
                "project_id": str(self.project.id),
                "date": "2026-05-25",
                "start_time": "11:00",
                "end_time": "09:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overlapping_work_session_returns_400(self):
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-25",
            start_time="09:00",
            end_time="11:00",
            duration_minutes=120,
        )
        response = self.client.post(
            self.work_sessions_url,
            {
                "project_id": str(self.project.id),
                "date": "2026-05-25",
                "start_time": "10:00",
                "end_time": "12:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_only_sees_own_work_sessions(self):
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
            project=self.other_project,
            date="2026-05-25",
            start_time="12:00",
            end_time="14:00",
            duration_minutes=120,
        )
        response = self.client.get(self.work_sessions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["project_id"], str(self.project.id))

    def test_list_work_sessions_returns_paginated_response(self):
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
            date="2026-05-25",
            start_time="10:30",
            end_time="11:30",
            duration_minutes=60,
        )

        response = self.client.get(f"{self.work_sessions_url}?page=1&per_page=1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertIn("pagination", response.data)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["pagination"]["page"], 1)
        self.assertEqual(response.data["pagination"]["per_page"], 1)
        self.assertEqual(response.data["pagination"]["total"], 2)
        self.assertEqual(response.data["pagination"]["total_pages"], 2)

    def test_filter_work_sessions_by_project_id(self):
        another_project = Project.objects.create(
            user=self.user, name="Otro proyecto", color="#10B981"
        )
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
            project=another_project,
            date="2026-05-25",
            start_time="10:30",
            end_time="11:30",
            duration_minutes=60,
        )

        response = self.client.get(
            f"{self.work_sessions_url}?project_id={self.project.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["project_id"], str(self.project.id))

    def test_filter_work_sessions_by_date(self):
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-24",
            start_time="09:00",
            end_time="10:00",
            duration_minutes=60,
        )
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-25",
            start_time="10:30",
            end_time="11:30",
            duration_minutes=60,
        )

        response = self.client.get(f"{self.work_sessions_url}?date=2026-05-25")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["date"], "2026-05-25")

    def test_filter_work_sessions_by_range(self):
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-24",
            start_time="09:00",
            end_time="10:00",
            duration_minutes=60,
        )
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-25",
            start_time="10:30",
            end_time="11:30",
            duration_minutes=60,
        )
        WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-26",
            start_time="12:00",
            end_time="13:00",
            duration_minutes=60,
        )

        response = self.client.get(
            f"{self.work_sessions_url}?from=2026-05-25&to=2026-05-26"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 2)

    def test_invalid_page_returns_400(self):
        response = self.client.get(f"{self.work_sessions_url}?page=0")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_invalid_per_page_returns_400(self):
        response = self.client.get(f"{self.work_sessions_url}?per_page=0")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_per_page_greater_than_100_returns_400(self):
        response = self.client.get(f"{self.work_sessions_url}?per_page=101")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_non_integer_pagination_returns_400(self):
        response = self.client.get(f"{self.work_sessions_url}?page=uno&per_page=dos")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_user_cannot_update_other_user_work_session(self):
        work_session = WorkSession.objects.create(
            user=self.other_user,
            project=self.other_project,
            date="2026-05-25",
            start_time="09:00",
            end_time="11:00",
            duration_minutes=120,
        )
        response = self.client.patch(
            self.work_session_detail_url(work_session),
            {"notes": "Intento de modificar sesión ajena"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_id_and_date_cannot_be_updated(self):
        work_session = WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-25",
            start_time="09:00",
            end_time="11:00",
            duration_minutes=120,
        )
        response = self.client.patch(
            self.work_session_detail_url(work_session), {"date": "2026-05-26"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duration_is_recalculated_when_times_are_updated(self):
        work_session = WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-25",
            start_time="09:00",
            end_time="11:00",
            duration_minutes=120,
        )
        response = self.client.patch(
            self.work_session_detail_url(work_session),
            {"start_time": "09:00", "end_time": "12:30"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["duration_minutes"], 210)
        work_session.refresh_from_db()
        self.assertEqual(work_session.duration_minutes, 210)

    def test_user_can_delete_own_work_session(self):
        work_session = WorkSession.objects.create(
            user=self.user,
            project=self.project,
            date="2026-05-25",
            start_time="09:00",
            end_time="11:00",
            duration_minutes=120,
        )
        response = self.client.delete(self.work_session_detail_url(work_session))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WorkSession.objects.count(), 0)
