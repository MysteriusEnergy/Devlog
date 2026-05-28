from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone

from apps.sessions.models import WorkSession


def get_summary(user, from_date=None, to_date=None):
    queryset = WorkSession.objects.filter(user=user)

    if from_date:
        queryset = queryset.filter(date__gte=from_date)

    if to_date:
        queryset = queryset.filter(date__lte=to_date)
    total_minutes = queryset.aggregate(total=Sum("duration_minutes"))["total"] or 0

    project_breakdown = list(
        queryset.values("project_id")
        .annotate(total_minutes=Sum("duration_minutes"))
        .order_by("project_id")
    )

    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    weekly_minutes = (
        WorkSession.objects.filter(
            user=user,
            date__gte=week_start,
            date__lte=week_end,
        ).aggregate(total=Sum("duration_minutes"))["total"] or 0
    )

    return {
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 2),
        "weekly_minutes": weekly_minutes,
        "project_breakdown": [
            {
                "project_id": str(item["project_id"]),
                "total_minutes": item["total_minutes"],
            }
            for item in project_breakdown
        ],
    }
