from django.urls import path

from analytics.views import ExerciseEventView, FunnelView

urlpatterns = [
    path("events/", ExerciseEventView.as_view(), name="exercise-events"),
    path("funnel/", FunnelView.as_view(), name="exercise-funnel"),
]
