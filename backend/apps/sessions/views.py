from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.sessions.models import WorkSession
from apps.sessions.serializers import WorkSessionSerializer

class WorkSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)