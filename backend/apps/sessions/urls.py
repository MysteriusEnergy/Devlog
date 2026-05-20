from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.sessions.views import WorkSessionViewSet

router = DefaultRouter()
router.register(r"", WorkSessionViewSet, basename="work-session")

urlpatterns = [
    path("", include(router.urls)),
]
