from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import ExerciseEvent
from analytics.serializers import ExerciseEventSerializer


class ExerciseEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = request.data.copy()
        serializer = ExerciseEventSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)


class FunnelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ExerciseEvent.objects.all()
        exercise_id = request.query_params.get("exercise_id")
        if exercise_id:
            queryset = queryset.filter(exercise_id=exercise_id)

        funnel = queryset.values("exercise_id").annotate(
            starts=Count("id", filter=Q(event_type=ExerciseEvent.START)),
            completions=Count("id", filter=Q(event_type=ExerciseEvent.COMPLETE)),
            hints=Count("id", filter=Q(event_type=ExerciseEvent.HINT)),
            errors=Count("id", filter=Q(event_type=ExerciseEvent.ERROR)),
        )

        overall = queryset.aggregate(
            starts=Count("id", filter=Q(event_type=ExerciseEvent.START)),
            completions=Count("id", filter=Q(event_type=ExerciseEvent.COMPLETE)),
            hints=Count("id", filter=Q(event_type=ExerciseEvent.HINT)),
            errors=Count("id", filter=Q(event_type=ExerciseEvent.ERROR)),
        )

        return Response({"funnel": list(funnel), "totals": overall})
