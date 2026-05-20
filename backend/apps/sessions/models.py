import uuid
from django.conf import settings
from django.db import models


class WorkSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="work_sessions"
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="work_sessions"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(editable=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-start_time"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["project"]),
        ]

    def __str__(self):
        return f"{self.project.name} - {self.date}"