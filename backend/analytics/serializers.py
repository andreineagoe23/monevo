from rest_framework import serializers

from analytics.models import ExerciseEvent


class ExerciseEventSerializer(serializers.ModelSerializer):
    exercise_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ExerciseEvent
        fields = [
            "id",
            "session_id",
            "exercise_id",
            "event_type",
            "metadata",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        exercise_id = validated_data.pop("exercise_id")
        return ExerciseEvent.objects.create(
            exercise_id=exercise_id,
            **validated_data,
        )

    def validate_session_id(self, value):
        if not value:
            raise serializers.ValidationError("Session ID is required.")
        if len(value) > 64:
            raise serializers.ValidationError("Session ID is too long.")
        return value

    def validate_event_type(self, value):
        valid_types = {choice[0] for choice in ExerciseEvent.EVENT_CHOICES}
        if value not in valid_types:
            raise serializers.ValidationError("Invalid event type.")
        return value
