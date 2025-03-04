from rest_framework import viewsets, serializers, generics, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from .models import (UserProfile, Course, Lesson, Quiz, Path, UserProgress, Mission, MissionCompletion, Questionnaire, Tool, SimulatedSavingsAccount, Question, UserResponse, PathRecommendation, 
LessonCompletion, QuizCompletion, Reward, UserPurchase, Badge, UserBadge, Referral, FriendRequest, Exercise, UserExerciseProgress)
from .serializers import (
    UserProfileSerializer, CourseSerializer, LessonSerializer, 
    QuizSerializer, PathSerializer, RegisterSerializer, UserProgressSerializer, LeaderboardSerializer, UserProfileSettingsSerializer, QuestionnaireSerializer, 
    ToolSerializer, SimulatedSavingsAccountSerializer,
    QuestionSerializer, UserResponseSerializer, PathRecommendationSerializer, RewardSerializer, UserPurchaseSerializer, BadgeSerializer,
    UserBadgeSerializer, ReferralSerializer, UserSearchSerializer, FriendRequestSerializer, ExerciseSerializer, UserExerciseProgressSerializer
)
from core.dialogflow import detect_intent_from_text, perform_web_search
from django.utils import timezone
from django.utils.timezone import now
import logging
import os
from decimal import Decimal
from django.middleware.csrf import get_token
from django.http import JsonResponse
import logging
from django.db import transaction
from django.db.models import F

logger = logging.getLogger(__name__)

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({"csrfToken": token})

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        progress = UserProgress.objects.filter(user=request.user).first()

        is_completed = UserResponse.objects.filter(user=request.user).exists()

        user_data = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "username": request.user.username,
            "email_reminders": user_profile.email_reminders,
            "earned_money": float(user_profile.earned_money),
            "points": user_profile.points,
        }

        return Response({
            "user_data": user_data,
            "streak": progress.streak if progress else 0,
            "profile_avatar": user_profile.profile_avatar,
            "is_questionnaire_completed": is_completed, 
            "referral_code": user_profile.referral_code,
        })


    def patch(self, request):
        user_profile = request.user.userprofile
        email_reminders = request.data.get('email_reminders')
        if email_reminders is not None:
            user_profile.email_reminders = email_reminders
            user_profile.save()
        return Response({"message": "Profile updated successfully."})


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            referral_code = serializer.validated_data.pop('referral_code', None)
            user = serializer.save()
            
            if referral_code:
                try:
                    referrer_profile = UserProfile.objects.get(referral_code=referral_code)
                    Referral.objects.create(
                        referrer=referrer_profile.user,
                        referred_user=user
                    )
                    # Award points
                    referrer_profile.add_points(100)
                    user.userprofile.add_points(50)
                except UserProfile.DoesNotExist:
                    pass

            return Response({
                "next": "/questionnaire/" if user.userprofile.wants_personalized_path else "/dashboard/"
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from core.tokens import set_jwt_cookies, delete_jwt_cookies


class CookieTokenObtainPairView(TokenObtainPairView):
    """Handles Login and Stores JWT in HTTP-only Cookies"""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            response = set_jwt_cookies(response, access_token, refresh_token)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        return response


class LogoutView(APIView):
    """Handles Logout and Clears JWT Cookies"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = JsonResponse({"message": "Logout successful."})
        return delete_jwt_cookies(response)



from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

class PathViewSet(viewsets.ModelViewSet):
    queryset = Path.objects.all()
    serializer_class = PathSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=["post"], url_path="add-generated-image")
    def add_generated_image(self, request):
        user_profile = request.user.userprofile
        image = request.FILES.get('image')

        if not image:
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Save image to storage
        file_path = default_storage.save(f'generated_images/{image.name}', ContentFile(image.read()))

        # Add file path to user's profile
        user_profile.add_generated_image(file_path)

        return Response({"message": "Image added successfully!", "file_path": file_path}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="get-generated-images")
    def get_generated_images(self, request):
        user_profile = request.user.userprofile
        return Response({"generated_images": user_profile.generated_images})

    @action(detail=False, methods=["post"], url_path="save-avatar")
    def save_avatar(self, request):
        user_profile = request.user.userprofile
        avatar_url = request.data.get("avatar_url")

        if not avatar_url:
            return Response({"error": "Avatar URL is missing."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.profile_avatar = avatar_url
        user_profile.save()
        return Response({"message": "Avatar saved successfully.", "avatar_url": avatar_url})

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_avatar(request):
    """Update user's avatar"""
    avatar_url = request.data.get('profile_avatar')
    
    if not avatar_url or not (
        avatar_url.startswith('https://avatars.dicebear.com/') or 
        avatar_url.startswith('https://api.dicebear.com/')
    ):
        return Response(
            {"error": "Invalid avatar URL. Only DiceBear avatars are allowed."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user_profile = request.user.userprofile
    user_profile.profile_avatar = avatar_url
    user_profile.save()
    
    return Response({"status": "success", "avatar_url": avatar_url})

from .utils import check_and_award_badge

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
        check_and_award_badge(request.user, 'lessons_completed')

        completed_lesson_ids = (
            user_progress.completed_lessons.values_list("id", flat=True) if user_progress else []
        )

        lesson_data = [
            {
                "id": lesson.id,
                "title": lesson.title,
                "short_description": lesson.short_description,
                "detailed_content": lesson.detailed_content,
                "video_url": lesson.video_url,
                "exercise_type": lesson.exercise_type,
                "exercise_data": lesson.exercise_data,
                "accessible": lesson.id in completed_lesson_ids or lesson.id == lessons.first().id,
                "is_completed": lesson.id in completed_lesson_ids,
            }
            for lesson in lessons
        ]

        return Response(lesson_data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def complete(self, request):
        lesson_id = request.data.get('lesson_id')
        user = request.user

        try:
            lesson = Lesson.objects.get(id=lesson_id)
            user_progress, created = UserProgress.objects.get_or_create(
                user=user, course=lesson.course
            )
            user_progress.completed_lessons.add(lesson)
            user_progress.save()

            user_profile = user.userprofile
            user_profile.add_money(5.00)  
            user_profile.add_points(10)    
            user_profile.save()

            total_lessons = lesson.course.lessons.count()
            completed_lessons = user_progress.completed_lessons.count()
            if completed_lessons == total_lessons:
                user_progress.mark_course_complete()

            return Response({"message": "Lesson completed!"}, status=status.HTTP_200_OK)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)


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

        try:
            quiz = Quiz.objects.get(id=quiz_id)
            if quiz.correct_answer == selected_answer:
                QuizCompletion.objects.create(user=request.user, quiz=quiz)

                user_profile = request.user.userprofile
                user_profile.add_money(10.00) 
                user_profile.add_points(20)    
                user_profile.save()

                return Response({"message": "Quiz completed!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Incorrect answer."}, status=status.HTTP_400_BAD_REQUEST)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)


class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]


    def check_path_completion(self, user, course):
        path = course.path
        if not path:
            return

        courses_in_path = Course.objects.filter(path=path)
        completed_courses = UserProgress.objects.filter(
            user=user,
            course__in=courses_in_path,
            is_course_complete=True
        ).count()

        if completed_courses == courses_in_path.count():
            user_profile = user.userprofile
            user_profile.add_money(100.00) 
            user_profile.add_points(200)    
            user_profile.save()

    @action(detail=False, methods=['post'], url_path='complete')
    def complete(self, request):
        lesson_id = request.data.get('lesson_id')
        if not lesson_id:
            return Response({"error": "lesson_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
            course = lesson.course
            user_profile = request.user.userprofile
            user_progress, created = UserProgress.objects.get_or_create(user=request.user, course=course)
            user_progress.completed_lessons.add(lesson)
            user_profile.add_money(Decimal('5.00'))
            user_profile.save()

            total_lessons = course.lessons.count()
            completed_lessons = user_progress.completed_lessons.count()
            if completed_lessons == total_lessons:

                user_profile.add_money(Decimal('50.00'))
                user_profile.add_points(50)
                user_profile.save()

                path = course.path
                if path:
                    courses_in_path = Course.objects.filter(path=path)
                    completed_courses = UserProgress.objects.filter(
                        user=request.user,
                        course__in=courses_in_path,
                        is_course_complete=True
                    ).count()

                    if completed_courses == courses_in_path.count():
                        user_profile.add_money(Decimal('100.00'))
                        user_profile.add_points(100)
                        user_profile.save()

            user_progress.update_streak()
            self.check_path_completion(user, course)

            return Response(
                {"status": "Lesson completed", "streak": user_progress.streak},
                status=status.HTTP_200_OK
            )
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

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
        try:
            top_profiles = UserProfile.objects.all().order_by('-points')[:10]
            serializer = LeaderboardSerializer(top_profiles, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Leaderboard error: {str(e)}")
            return Response({"error": str(e)}, status=500)

class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        return Response({
            "email_reminders": user_profile.email_reminders,
            "email_frequency": user_profile.email_frequency,
            "profile": {
                "username": request.user.username,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "dark_mode": user_profile.dark_mode,
            },
        })

    def patch(self, request):
        user_profile = request.user.userprofile
        email_reminders = request.data.get('email_reminders')
        email_frequency = request.data.get('email_frequency')
        dark_mode = request.data.get('dark_mode')
        
        if dark_mode is not None:
            user_profile.dark_mode = dark_mode
            user_profile.save()

        if email_reminders is not None:
            user_profile.email_reminders = email_reminders

        if email_frequency in ['daily', 'weekly', 'monthly']:
            user_profile.email_frequency = email_frequency

        user_profile.save()
        return Response({"message": "Settings updated successfully."})



class MissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            # Fetch daily and weekly missions
            daily_completions = MissionCompletion.objects.filter(
                user=user, mission__mission_type="daily"
            )
            weekly_completions = MissionCompletion.objects.filter(
                user=user, mission__mission_type="weekly"
            )

            daily_missions = []
            weekly_missions = []

            for completion in daily_completions:
                daily_missions.append({
                    "id": completion.mission.id,
                    "name": completion.mission.name,
                    "description": completion.mission.description,
                    "points_reward": completion.mission.points_reward,
                    "progress": completion.progress,
                    "status": completion.status,
                    "goal_type": completion.mission.goal_type,
                })

            for completion in weekly_completions:
                weekly_missions.append({
                    "id": completion.mission.id,
                    "name": completion.mission.name,
                    "description": completion.mission.description,
                    "points_reward": completion.mission.points_reward,
                    "progress": completion.progress,
                    "status": completion.status,
                    "goal_type": completion.mission.goal_type,
                })

            return Response({
                "daily_missions": daily_missions,
                "weekly_missions": weekly_missions,
            }, status=200)

        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching missions."},
                status=500,
            )

    def post(self, request, mission_id):
        user = request.user
        try:
            # Find the specific MissionCompletion record
            mission_completion = MissionCompletion.objects.get(user=user, mission_id=mission_id)
            increment = request.data.get("progress", 0)

            if not isinstance(increment, int):
                return Response({"error": "Progress must be an integer."}, status=400)

            # Update mission progress
            mission_completion.update_progress(increment)
            return Response({"message": "Mission progress updated.", "progress": mission_completion.progress}, status=200)

        except MissionCompletion.DoesNotExist:
            return Response({"error": "Mission not found for this user."}, status=404)
        except Exception as e:
            logging.error(f"Error updating mission progress for user {user.username}: {str(e)}")
            return Response({"error": "An error occurred while updating mission progress."}, status=500)


class SavingsAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account, _ = SimulatedSavingsAccount.objects.get_or_create(user=request.user)
        return Response({"balance": account.balance}, status=200)

    def post(self, request):
        amount = request.data.get("amount", 0)
        try:
            account, _ = SimulatedSavingsAccount.objects.get_or_create(user=request.user)
            account.add_to_balance(amount)

            # Update savings-related missions
            mission_completions = MissionCompletion.objects.filter(
                user=request.user,
                mission__goal_type="add_savings"
            )
            for mission_completion in mission_completions:
                mission_completion.update_progress(increment=amount, total=100)

            return Response(
                {"message": "Savings added successfully!", "balance": account.balance},
                status=200,
            )
        except Exception as e:
            logging.error(f"Error updating savings for user {request.user.username}: {str(e)}")
            return Response({"error": "An error occurred while updating savings."}, status=500)



class FinanceFactView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Update fact-related missions
            mission_completions = MissionCompletion.objects.filter(
                user=request.user,
                mission__goal_type="read_fact"
            )
            for mission_completion in mission_completions:
                if mission_completion.progress < 100:
                    mission_completion.update_progress(100, total=100)

            return Response({"message": "Fact read successfully!"}, status=200)
        except Exception as e:
            logging.error(f"Error marking fact read for user {request.user.username}: {str(e)}")
            return Response({"error": "An error occurred while marking the fact as read."}, status=500)



import os
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .dialogflow import detect_intent_from_text, perform_web_search

class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_input = request.data.get("text", "")
        session_id = str(request.user.id)

        if not user_input:
            return Response({"error": "No input provided"}, status=400)

        try:
            project_id = os.environ.get("DIALOGFLOW_PROJECT_ID", "monevo-443011")
            response_text = detect_intent_from_text(
                project_id=project_id,
                text=user_input,
                session_id=session_id
            )
            return Response({"response": response_text}, status=200)
        except Exception as e:
            print("Dialogflow Error:", e)
            return Response({"error": str(e)}, status=500)

    @staticmethod
    def dialogflow_webhook(request):
        """
        Handle requests from Dialogflow's webhook.
        """
        try:
            req = json.loads(request.body)
            intent_name = req.get("queryResult", {}).get("intent", {}).get("displayName")

            if intent_name == "SearchTheWeb":
                search_query = req.get("queryResult", {}).get("queryText", "")
                response_text = perform_web_search(search_query)
            else:
                response_text = f"Intent '{intent_name}' is not implemented yet."

            return JsonResponse({
                "fulfillmentText": response_text
            })

        except Exception as e:
            return JsonResponse({
                "fulfillmentText": f"An error occurred: {str(e)}"
            })


class ToolListView(APIView):
    """
    API Endpoint to list tool categories only.
    """
    def get(self, request):
        tools = [
            {"category": "Forex Tools"},
            {"category": "Crypto Tools"},
            {"category": "News & Calendars"},
            {"category": "Basic Finance & Budgeting Tools"},
        ]
        return Response(tools)


class SavingsGoalCalculatorView(APIView):
    """
    API Endpoint to calculate savings goals based on compound interest.
    """
    def post(self, request):
        try:
            data = request.data
            savings_goal = float(data.get('savings_goal', 0))
            initial_investment = float(data.get('initial_investment', 0))
            years_to_grow = float(data.get('years_to_grow', 0))
            annual_interest_rate = float(data.get('annual_interest_rate', 0)) / 100
            compound_frequency = int(data.get('compound_frequency', 1))

            if years_to_grow <= 0 or compound_frequency <= 0:
                return Response({"error": "Invalid input for years or frequency."}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate the final savings using compound interest formula
            final_savings = initial_investment * ((1 + annual_interest_rate / compound_frequency) ** (compound_frequency * years_to_grow))

            return Response({
                "final_savings": round(final_savings, 2),
                "message": f"To achieve your savings goal of {savings_goal}, your estimated final savings would be {round(final_savings, 2)}."
            })
        except ValueError:
            return Response({"error": "Invalid input values."}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:3000/monevo#/password-reset/{uid}/{token}"

            # Render the email content
            context = {
                'user': user,
                'reset_link': reset_link,
            }
            subject = "Password Reset Request"
            html_content = render_to_string("emails/password_reset.html", context)
            text_content = strip_tags(html_content)  # Fallback for plain-text email clients

            # Send the email
            email_message = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "No user found with this email."}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid user ID or token."}, status=status.HTTP_400_BAD_REQUEST)

        if PasswordResetTokenGenerator().check_token(user, token):
            return Response({"message": "Token is valid, proceed with password reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid user ID or token."}, status=status.HTTP_400_BAD_REQUEST)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

class QuestionnaireView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        questions = Question.objects.order_by('order')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        answers = request.data.get('answers', {})
        user = request.user if request.user.is_authenticated else None

        for question_id, answer in answers.items():
            try:
                question = Question.objects.get(id=question_id)
                UserResponse.objects.create(user=user, question=question, answer=answer)
            except Question.DoesNotExist:
                return Response({"error": f"Question {question_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Questionnaire submitted successfully."}, status=status.HTTP_201_CREATED)


class RecommendationView(APIView):
    def get(self, request, user_id):
        responses = UserResponse.objects.filter(user_id=user_id)
        recommended_path = None

        recommendations = {
            "Basic Finance": "It looks like you're interested in budgeting and saving. Start with Basic Finance to build strong financial habits!",
            "Crypto": "You've mentioned crypto or blockchain. Our Crypto path will guide you through the fundamentals of digital assets.",
            "Real Estate": "Since you showed interest in real estate, we recommend the Real Estate path to explore property investment.",
            "Forex": "Your responses indicate interest in currency trading. The Forex path will help you master trading strategies.",
            "Personal Finance": "Want to improve overall financial wellness? The Personal Finance path is the best place to start!",
            "Financial Mindset": "A strong mindset is key to financial success! Learn about wealth psychology with the Financial Mindset path."
        }

        for response in responses:
            for path, message in recommendations.items():
                if path.lower() in response.answer.lower():
                    recommended_path = path
                    recommendation_message = message
                    break

        if not recommended_path:
            recommended_path = "Basic Finance"
            recommendation_message = "Start with Basic Finance to strengthen your foundation in money management."

        return Response({
            "path": recommended_path,
            "message": recommendation_message
        })


class QuestionnaireSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        answers = request.data.get('answers', {})

        if not answers:
            return Response({"error": "No answers provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            for question_id, answer in answers.items():
                question = Question.objects.get(id=question_id)
                UserResponse.objects.create(user=user, question=question, answer=answer)

            user_profile = UserProfile.objects.get(user=user)
            user_profile.wants_personalized_path = True
            user_profile.save()

            return Response({"message": "Questionnaire submitted successfully."}, status=status.HTTP_201_CREATED)

        except Question.DoesNotExist:
            return Response({"error": "Invalid question ID."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error in QuestionnaireSubmitView: {e}")
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import logging
import json
from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Course, Path, UserResponse, UserProfile
from .serializers import CourseSerializer

logger = logging.getLogger(__name__)

class PersonalizedPathView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        responses = UserResponse.objects.filter(user=user)
        if not responses.exists():
            return Response({"error": "No questionnaire responses found."}, status=404)

        path_keywords = {
            "Financial Mindset": ["mindset", "psychology", "discipline", "growth"],
            "Personal Finance": ["budget", "saving", "spending", "invest"],
            "Forex": ["forex", "currency", "trading"],
            "Crypto": ["crypto", "bitcoin", "blockchain"],
            "Real Estate": ["real estate", "property", "housing"],
            "Basic Finance": ["finance", "credit", "debt", "investment"],
        }

        path_scores = defaultdict(int)
        for response in responses:
            for path, keywords in path_keywords.items():
                if any(keyword in response.answer.lower() for keyword in keywords):
                    path_scores[path] += 1

        sorted_paths = sorted(path_scores.items(), key=lambda x: x[1], reverse=True)

        selected_courses = []
        used_paths = set()
        total_courses_needed = 10

        for path_name, _ in sorted_paths:
            path_obj = Path.objects.filter(title=path_name).first()
            if path_obj and path_obj.id not in used_paths:
                courses = list(Course.objects.filter(path=path_obj)[:2])
                selected_courses.extend(courses)
                used_paths.add(path_obj.id)

            if len(selected_courses) >= total_courses_needed:
                break 

        if len(selected_courses) < total_courses_needed:
            remaining_courses = list(
                Course.objects.exclude(id__in=[c.id for c in selected_courses])[:total_courses_needed - len(selected_courses)]
            )
            selected_courses.extend(remaining_courses)

        if not selected_courses:
            return Response({"error": "No suitable courses found for your preferences."}, status=404)
        

        serializer = CourseSerializer(
            selected_courses, 
            many=True, 
            context={'request': request}
        )

        return Response({
            "personalized_courses": serializer.data,
            "message": "We've assembled a custom learning path based on your interests."
        })


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Lesson, UserProgress

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exercise_progress(request, exercise_id):
    try:
        lesson = Lesson.objects.get(id=exercise_id)
        user_progress = UserProgress.objects.filter(user=request.user, course=lesson.course).first()

        if user_progress:
            return Response({
                "completed": lesson in user_progress.completed_lessons.all(),
                "answers": {}  # Add logic to fetch saved answers if applicable
            })
        else:
            return Response({"completed": False, "answers": {}})
    except Lesson.DoesNotExist:
        return Response({"error": "Exercise not found."}, status=404)


class RecentActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        activities = []

        # Lesson completions
        lesson_completions = LessonCompletion.objects.filter(
            user_progress__user=user
        ).select_related('lesson', 'user_progress__course')
        for lc in lesson_completions:
            activities.append({
                "type": "lesson",
                "action": "completed",
                "title": lc.lesson.title,
                "course": lc.user_progress.course.title,
                "timestamp": lc.completed_at
            })

        # Quiz completions
        quiz_completions = QuizCompletion.objects.filter(user=user).select_related('quiz')
        for qc in quiz_completions:
            activities.append({
                "type": "quiz",
                "action": "completed",
                "title": qc.quiz.title,
                "timestamp": qc.completed_at
            })

        # Mission completions
        missions = MissionCompletion.objects.filter(
            user=user, 
            status='completed'
        ).exclude(completed_at__isnull=True)
        for mc in missions:
            activities.append({
                "type": "mission",
                "action": "completed",
                "name": mc.mission.name,
                "timestamp": mc.completed_at
            })

        # Course completions
        course_completions = UserProgress.objects.filter(
            user=user,
            is_course_complete=True
        ).exclude(course_completed_at__isnull=True)
        for cc in course_completions:
            activities.append({
                "type": "course",
                "action": "completed",
                "title": cc.course.title,
                "timestamp": cc.course_completed_at
            })

        sorted_activities = sorted(
            activities, 
            key=lambda x: x["timestamp"], 
            reverse=True
        )[:5]

        return Response({"recent_activities": sorted_activities})

class RewardViewSet(viewsets.ModelViewSet):
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        reward_type = self.kwargs.get('type', None)
        queryset = Reward.objects.filter(is_active=True)
        
        if reward_type in ['shop', 'donate']:
            queryset = queryset.filter(type=reward_type)
            
        return queryset

        
class UserPurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = UserPurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPurchase.objects.filter(user=self.request.user)

    def create(self, request):
        try:
            # Validate required fields
            reward_id = request.data.get('reward_id')
            if not reward_id:
                return Response({"error": "Missing reward_id"}, status=400)

            # Get objects
            user_profile = request.user.userprofile
            reward = Reward.objects.get(id=reward_id, is_active=True)

            # Validate balance
            if user_profile.earned_money < reward.cost:
                return Response({"error": "Insufficient funds"}, status=400)

            # Process transaction
            user_profile.earned_money -= reward.cost
            user_profile.save()

            # Create purchase record
            purchase = UserPurchase.objects.create(
                user=request.user,
                reward=reward
            )

            return Response({
                "message": "Transaction successful!",
                "remaining_balance": float(user_profile.earned_money),
                "purchase": UserPurchaseSerializer(purchase).data
            }, status=201)

        except Reward.DoesNotExist:
            return Response({"error": "Reward not found or inactive"}, status=404)
        except Exception as e:
            logger.error(f"Purchase error: {str(e)}")
            return Response({"error": "Server error processing transaction"}, status=500)


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.filter(is_active=True)
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

class UserBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)


class ReferralView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            referrals = Referral.objects.filter(referrer=request.user)
            serializer = ReferralSerializer(referrals, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching referrals: {str(e)}")
            return Response({"error": "Error fetching referrals"}, status=500)

    def post(self, request):
        referral_code = request.data.get('referral_code', '').strip().upper()
        
        if not referral_code:
            return Response({"error": "Referral code is required"}, status=400)

        try:
            referrer_profile = UserProfile.objects.get(referral_code=referral_code)
            
            if referrer_profile.user == request.user:
                return Response({"error": "You cannot use your own referral code"}, status=400)
            
            if Referral.objects.filter(referred_user=request.user).exists():
                return Response({"error": "You already used a referral code"}, status=400)

            # Create referral
            Referral.objects.create(
                referrer=referrer_profile.user,
                referred_user=request.user
            )

            # Add points using atomic transactions
            with transaction.atomic():
                UserProfile.objects.filter(pk=referrer_profile.pk).update(
                    points=F('points') + 100
                )
                UserProfile.objects.filter(user=request.user).update(
                    points=F('points') + 50
                )

            return Response({"message": "Referral applied successfully!"})
            
        except UserProfile.DoesNotExist:
            return Response({"error": "Invalid referral code"}, status=400)
        except Exception as e:
            logger.error(f"Referral error: {str(e)}")
            return Response({"error": "Server error processing referral"}, status=500)

class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            search_query = request.query_params.get('search', '').strip()
            
            if not search_query or len(search_query) < 3:
                return Response({"error": "Search query must be at least 3 characters"}, status=400)

            users = User.objects.filter(
                username__icontains=search_query
            ).exclude(id=request.user.id)[:5]
            
            serializer = UserSearchSerializer(users, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"User search error: {str(e)}")
            return Response({"error": "Error processing search"}, status=500)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FriendRequest

class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get pending requests where the current user is the receiver
        requests = FriendRequest.objects.filter(
            receiver=request.user,
            status='pending'
        )
        serializer = FriendRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        receiver_id = request.data.get("receiver")  # Ensure correct key

        if not receiver_id:
            return Response({"error": "Receiver ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(id=receiver_id)

            # Prevent sending requests to oneself
            if request.user == receiver:
                return Response({"error": "You cannot send a request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a request already exists
            existing_request = FriendRequest.objects.filter(sender=request.user, receiver=receiver, status="pending")
            if existing_request.exists():
                return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new friend request
            FriendRequest.objects.create(sender=request.user, receiver=receiver)
            return Response({"message": "Friend request sent successfully"}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        action = request.data.get("action") 

        if action not in ["accept", "reject"]:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            friend_request = FriendRequest.objects.get(id=pk, receiver=request.user)

            if action == "accept":
                friend_request.status = "accepted"
                friend_request.save()
                return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)

            elif action == "reject":
                friend_request.status = "rejected"
                friend_request.save()
                return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)

        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

class FriendsLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = User.objects.filter(
            id__in=FriendRequest.objects.filter(
                sender=request.user, status="accepted"
            ).values_list("receiver_id", flat=True)
        ) | User.objects.filter(
            id__in=FriendRequest.objects.filter(
                receiver=request.user, status="accepted"
            ).values_list("sender_id", flat=True)
        )

        friend_profiles = UserProfile.objects.filter(user__in=friends).order_by("-points")
        serializer = LeaderboardSerializer(friend_profiles, many=True)
        return Response(serializer.data)


# Add to views.py
from rest_framework.decorators import action
from rest_framework.response import Response

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        exercise_type = self.request.query_params.get('type')
        category = self.request.query_params.get('category')
        difficulty = self.request.query_params.get('difficulty')
        
        if exercise_type:
            queryset = queryset.filter(type=exercise_type)
        if category:
            queryset = queryset.filter(category__iexact=category)
        if difficulty:
            queryset = queryset.filter(difficulty__iexact=difficulty)
        return queryset

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        exercise = self.get_object()
        user_answer = request.data.get('user_answer')
        
        progress, created = UserExerciseProgress.objects.get_or_create(
            user=request.user,
            exercise=exercise,
            defaults={'user_answer': user_answer}
        )
        
        progress.attempts += 1
        progress.user_answer = user_answer
        progress.completed = (user_answer == exercise.correct_answer)
        progress.save()
        
        return Response({
            'correct': progress.completed,
            'correct_answer': exercise.correct_answer,
            'attempts': progress.attempts
        })

class UserExerciseProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserExerciseProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserExerciseProgress.objects.filter(user=self.request.user)