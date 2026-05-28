from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.analytics.services.summary import get_summary


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def summary(request):
    from_date = request.query_params.get("from")
    to_date = request.query_params.get("to")

    data = get_summary(
        user=request.user,
        from_date=from_date,
        to_date=to_date,
    )

    return Response(data)
