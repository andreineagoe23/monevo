from rest_framework import viewsets, serializers, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import UserProfile, Course, Lesson, Quiz, Path, UserProgress
from .serializers import (
    UserProfileSerializer, CourseSerializer, LessonSerializer, 
    QuizSerializer, PathSerializer, RegisterSerializer, UserProgressSerializer
)
from rest_framework.parsers import MultiPartParser, FormParser

# User profile view
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        user_data = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "username": request.user.username,
            "email_reminders": user_profile.email_reminders,  # Include in response
        }
        return Response(user_data)

    def patch(self, request):
        user_profile = request.user.userprofile
        email_reminders = request.data.get('email_reminders')
        if email_reminders is not None:
            user_profile.email_reminders = email_reminders
            user_profile.save()
        return Response({"message": "Profile updated successfully."})


# User registration view
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class PathViewSet(viewsets.ModelViewSet):
    queryset = Path.objects.all()
    serializer_class = PathSerializer

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=["put"], url_path="update")
    def update_profile(self, request):
        user = request.user
        data = request.data

        # Update User fields
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)

        # Update profile picture if provided
        profile = user.userprofile
        if "profile_picture" in request.FILES:
            profile.profile_picture = request.FILES["profile_picture"]

        user.save()
        profile.save()

        return Response({"message": "Profile updated successfully!"}, status=200)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def with_progress(self, request):
        course_id = request.query_params.get("course", None)
        if not course_id:
            return Response({"error": "Course ID is required."}, status=400)

        lessons = self.get_queryset().filter(course_id=course_id)
        user_progress = UserProgress.objects.filter(user=request.user, course_id=course_id).first()

        completed_lesson_ids = (
            user_progress.completed_lessons.values_list("id", flat=True) if user_progress else []
        )

        lesson_data = [
            {
                "id": lesson.id,
                "title": lesson.title,
                "short_description": lesson.short_description,
                "detailed_content": lesson.detailed_content,
                "accessible": lesson.id in completed_lesson_ids or lesson.id == lessons.first().id,
                "is_completed": lesson.id in completed_lesson_ids,
            }
            for lesson in lessons
        ]

        return Response(lesson_data)

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        course_id = self.request.query_params.get("course")
        if not course_id:
            return Quiz.objects.none()

        # Check if the user has completed the course
        user_progress = UserProgress.objects.filter(user=user, course_id=course_id, is_course_complete=True).first()
        if user_progress:
            return Quiz.objects.filter(course_id=course_id)
        return Quiz.objects.none()
            

class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='complete')
    def complete(self, request):
        lesson_id = request.data.get('lesson_id')
        if not lesson_id:
            return Response({"error": "lesson_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

        course = lesson.course

        # Create a UserProgress entry for the course if it doesn't already exist
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            course=course
        )

        # Add the completed lesson to the progress
        user_progress.completed_lessons.add(lesson)

        # Check if all lessons are completed for the current course
        all_lessons = course.lessons.all()
        if set(user_progress.completed_lessons.all()) == set(all_lessons):
            user_progress.is_course_complete = True

        user_progress.save()

        return Response(
            {"status": "Lesson completed", "is_course_complete": user_progress.is_course_complete},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"])
    def progress_summary(self, request):
        user = request.user
        progress_data = []

        user_progress = UserProgress.objects.filter(user=user)
        for progress in user_progress:
            total_lessons = progress.course.lessons.count()
            completed_lessons = progress.completed_lessons.count()
            percent_complete = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0

            progress_data.append({
                "path": progress.course.path.title if progress.course.path else None,
                "course": progress.course.title,
                "percent_complete": percent_complete,
            })

        return Response({"overall_progress": sum(d["percent_complete"] for d in progress_data) / len(progress_data) if progress_data else 0,
                         "paths": progress_data})