from django.conf import settings
from django.db import models


class ExerciseEvent(models.Model):
    START = "start"
    COMPLETE = "complete"
    HINT = "hint"
    ERROR = "error"

    EVENT_CHOICES = [
        (START, "Start"),
        (COMPLETE, "Complete"),
        (HINT, "Hint"),
        (ERROR, "Error"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exercise_events",
    )
    session_id = models.CharField(max_length=64)
    exercise = models.ForeignKey(
        "education.Exercise",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["exercise", "event_type", "created_at"]),
            models.Index(fields=["session_id", "created_at"]),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.exercise_id} ({self.session_id})"
