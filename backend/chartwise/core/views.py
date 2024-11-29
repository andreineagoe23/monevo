from rest_framework import viewsets, serializers, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import UserProfile, Course, Lesson, Quiz, Path, UserProgress, Mission, MissionCompletion, Questionnaire
from .serializers import (
    UserProfileSerializer, CourseSerializer, LessonSerializer, 
    QuizSerializer, PathSerializer, RegisterSerializer, UserProgressSerializer, LeaderboardSerializer, UserProfileSettingsSerializer, QuestionnaireSerializer
)
from rest_framework.parsers import MultiPartParser, FormParser


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        user_data = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "username": request.user.username,  # Verify this is correct
            "email_reminders": user_profile.email_reminders,
            "earned_money": float(user_profile.earned_money),
            "points": user_profile.points,
        }
        print("User Data:", user_data)  # Debug log
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

        quizzes = Quiz.objects.filter(course_id=course_id)
        return quizzes

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def complete(self, request):
        quiz_id = request.data.get("quiz_id")
        selected_answer = request.data.get("selected_answer")

        if not quiz_id or not selected_answer:
            return Response({"error": "Quiz ID and selected answer are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

        if quiz.correct_answer == selected_answer:
            user_profile = request.user.userprofile
            user_profile.add_money(10.00)
            user_profile.add_points(20)
            return Response({"message": "Quiz completed successfully!", "earned_money": 10.00}, status=status.HTTP_200_OK)

        return Response({"message": "Incorrect answer. Try again!"}, status=status.HTTP_400_BAD_REQUEST)

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

        # Mark lesson as completed
        course = lesson.course
        user_profile = request.user.userprofile
        user_progress, created = UserProgress.objects.get_or_create(user=request.user, course=course)
        user_progress.completed_lessons.add(lesson)
        user_profile.add_money(5.00)
        user_profile.add_points(10)
        user_progress.save()

        # Check for mission completion and complete eligible missions
        missions_completed = self.check_and_complete_missions(request.user)

        return Response(
            {"status": "Lesson completed", "missions_completed": missions_completed},
            status=status.HTTP_200_OK
        )

    def check_and_complete_missions(self, user):
        """
        This method checks for missions that are marked as 'not_started' and completes them.
        """
        mission_completions = MissionCompletion.objects.filter(
            user=user,
            status='not_started',
        )
        completed_count = 0
        for mission_completion in mission_completions:
            mission_completion.status = 'completed'
            mission_completion.save()
            user.userprofile.add_points(mission_completion.mission.points_reward)
            completed_count += 1
        user.userprofile.save()
        return completed_count


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


class LeaderboardViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        top_users = UserProfile.objects.order_by('-points')[:10]
        serializer = LeaderboardSerializer(top_users, many=True)
        return Response(serializer.data)

class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSettingsSerializer(user_profile)
        return Response(serializer.data)

    def patch(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSettingsSerializer(
            user_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



class MissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            # Fetch and reset missions where needed
            completions = MissionCompletion.objects.filter(user=user)
            for completion in completions:
                completion.reset_daily_missions()
                completion.reset_monthly_missions()

            # Categorize missions
            daily_missions = Mission.objects.filter(mission_type="daily")
            monthly_missions = Mission.objects.filter(mission_type="monthly")

            def format_mission(mission, user):
                completion = MissionCompletion.objects.filter(user=user, mission=mission).first()
                return {
                    "id": mission.id,
                    "name": mission.name,
                    "description": mission.description,
                    "points_reward": mission.points_reward,
                    "status": completion.status if completion else "not_started",
                }

            response_data = {
                "daily": [format_mission(mission, user) for mission in daily_missions],
                "monthly": [format_mission(mission, user) for mission in monthly_missions],
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error fetching missions: {e}")  # Add this line for debugging
            return Response(
                {"error": "An error occurred while fetching missions."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, mission_id):
        user = request.user
        try:
            # Fetch the mission
            mission = Mission.objects.get(id=mission_id)
        except Mission.DoesNotExist:
            return Response({"message": "Mission not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the mission is already completed
        mission_completion, created = MissionCompletion.objects.get_or_create(
            user=user, mission=mission
        )

        if mission_completion.status == "completed":
            return Response({"message": "Mission already completed."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the mission as completed
        mission_completion.status = "completed"
        mission_completion.save()

        # Update user's profile points
        user.userprofile.add_points(mission.points_reward)
        user.userprofile.save()

        return Response({"message": "Mission completed successfully!"}, status=status.HTTP_200_OK)



class QuestionnaireView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the user's questionnaire data
        try:
            questionnaire = Questionnaire.objects.get(user=request.user)
            serializer = QuestionnaireSerializer(questionnaire)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Questionnaire.DoesNotExist:
            return Response({"message": "Questionnaire not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Create or update the user's questionnaire
        try:
            questionnaire, created = Questionnaire.objects.get_or_create(user=request.user)
            serializer = QuestionnaireSerializer(questionnaire, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
