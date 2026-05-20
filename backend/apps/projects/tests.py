from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User
from apps.projects.models import Project


class ProjectAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123"
        )
        self.projects_url = reverse("project-list")
        self.client.force_authenticate(user=self.user)


    def project_detail_url(self, project):
        return reverse("project-detail", kwargs={"pk": project.id})


    def test_authenticated_user_can_create_project(self):
        response = self.client.post(self.projects_url, {
            "name": "DevLog",
            "description": "Proyecto personal",
            "color": "#3B82F6"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().user, self.user)


    def test_unauthenticated_user_cannot_create_project(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(self.projects_url, {
            "name": "DevLog",
            "color": "#3B82F6"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_user_only_sees_own_projects(self):
        Project.objects.create(
            user=self.user,
            name="Mi proyecto",
            color="#3B82F6"
        )
        Project.objects.create(
            user=self.other_user,
            name="Proyecto ajeno",
            color="#EF4444"
        )

        response = self.client.get(self.projects_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Mi proyecto")


    def test_user_cannot_update_other_user_project(self):
        project = Project.objects.create(
            user=self.other_user,
            name="Proyecto ajeno",
            color="#EF4444"
        )

        response = self.client.patch(self.project_detail_url(project), {
            "name": "Hackeado"
        })

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_invalid_color_returns_400(self):
        response = self.client.post(self.projects_url, {
            "name": "DevLog",
            "color": "azul"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("color", response.data)
