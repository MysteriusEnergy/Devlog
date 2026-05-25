from math import ceil

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.sessions.models import WorkSession
from apps.sessions.serializers import WorkSessionSerializer

class WorkSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = WorkSession.objects.filter(user=self.request.user)

        project_id = self.request.query_params.get("project_id")
        date = self.request.query_params.get("date")
        from_date = self.request.query_params.get("from")
        to_date = self.request.query_params.get("to")

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        if date:
            queryset = queryset.filter(date=date)

        if from_date:
            queryset = queryset.filter(date__gte=from_date)

        if to_date:
            queryset = queryset.filter(date__lte=to_date)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        try:
            page = int(request.query_params.get("page", 1))
            per_page = int(request.query_params.get("per_page", 20))
        except ValueError:
            return Response(
                {"message": "page y per_page deben ser enteros"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if page < 1:
            return Response(
                {"message": "page debe ser mayor o igual a 1"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if per_page < 1 or per_page > 100:
            return Response(
                {"message": "per_page debe estar entre 1 y 100"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total = queryset.count()
        start = (page - 1) * per_page
        end = start + per_page

        serializer = self.get_serializer(queryset[start:end], many=True)

        return Response(
            {
                "data": serializer.data,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "total_pages": ceil(total / per_page) if total else 0,
                },
            },
            status=status.HTTP_200_OK,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
