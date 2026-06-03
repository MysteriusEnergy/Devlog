from rest_framework import serializers

from apps.projects.models import Project
from apps.sessions.models import WorkSession
from apps.sessions.services.work_sessions import ( calculate_duration_minutes, has_time_overlap, )


class WorkSessionSerializer(serializers.ModelSerializer):
    project_id = serializers.UUIDField()


    class Meta:
        model = WorkSession
        fields = [
            "id",
            "project_id",
            "date",
            "start_time",
            "end_time",
            "duration_minutes",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "duration_minutes",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        start_time = attrs.get("start_time", getattr(self.instance, "start_time", None))
        end_time = attrs.get("end_time", getattr(self.instance, "end_time", None))
        date = attrs.get("date", getattr(self.instance, "date", None))

        if start_time >= end_time:
            raise serializers.ValidationError(
                {"message": "start_time debe ser menor que end_time"}
            )

        if self.instance is None:
            project_id = attrs.pop("project_id", None)

            try:
                project = Project.objects.get(id=project_id, user=user)
            except Project.DoesNotExist:
                raise serializers.ValidationError(
                    {"project_id": "El proyecto no existe"}
                )

            attrs["project"] = project
        else:
            if "project_id" in attrs or "date" in attrs:
                raise serializers.ValidationError(
                    {"message": "project_id y date no se pueden editar"}
                )

        exclude_session_id = self.instance.id if self.instance else None

        if has_time_overlap(user, date, start_time, end_time, exclude_session_id):
            raise serializers.ValidationError(
                {"message": "La sesión se traslapa con otra sesión existente"}
            )

        attrs["duration_minutes"] = calculate_duration_minutes(start_time, end_time)
        return attrs
