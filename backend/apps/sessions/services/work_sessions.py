from datetime import datetime


def calculate_duration_minutes(start_time, end_time):
    start = datetime.combine(datetime.today(), start_time)
    end = datetime.combine(datetime.today(), end_time)
    return int((end - start).total_seconds() // 60)


def has_time_overlap(user, date, start_time, end_time, exclude_session_id=None):
    from apps.sessions.models import WorkSession

    queryset = WorkSession.objects.filter(
        user=user,
        date=date,
        start_time__lt=end_time,
        end_time__gt=start_time,
    )

    if exclude_session_id:
        queryset = queryset.exclude(id=exclude_session_id)

    return queryset.exists()
