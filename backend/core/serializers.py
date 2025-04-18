# core/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ( UserProfile, Course, Lesson, Quiz, Path, UserProgress, Questionnaire, Tool, Mission, MissionCompletion,
SimulatedSavingsAccount, Question, UserResponse, PathRecommendation, Reward, UserPurchase, Badge, UserBadge, Referral, FriendRequest, Exercise, UserExerciseProgress, LessonSection)

class RegisterSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'referral_code']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)

        # Only create User here - profile is created by signal
        user = User.objects.create_user(**validated_data)

        # Access profile created by signal
        user_profile = user.userprofile
        user_profile.save()

        if referral_code:
            try:
                referrer_profile = UserProfile.objects.get(referral_code=referral_code)
                Referral.objects.create(referrer=referrer_profile.user, referred_user=user)
                referrer_profile.add_points(100)
                user_profile.add_points(50)
            except UserProfile.DoesNotExist:
                pass

        return user


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'question', 'choices', 'correct_answer']

class LessonSectionSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = LessonSection
        fields = [
            'id', 'order', 'title', 'content_type',
            'text_content', 'video_url', 'exercise_type', 'exercise_data'
        ]

class LessonSerializer(serializers.ModelSerializer):
    sections = LessonSectionSerializer(many=True, read_only=True)
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'short_description', 'sections', 'is_completed']

    def get_is_completed(self, obj):
        completed_lesson_ids = self.context.get('completed_lesson_ids', [])
        return obj.id in completed_lesson_ids

class CourseSerializer(serializers.ModelSerializer):
    path_title = serializers.CharField(source='path.title')
    lessons = LessonSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    completed_lessons = serializers.SerializerMethodField()
    total_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'path', 'path_title', 'title', 'description', 'lessons', 'quizzes', 'image', 'completed_lessons', 'total_lessons']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_completed_lessons(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            progress = UserProgress.objects.filter(user=user, course=obj).first()
            return progress.completed_lessons.count() if progress else 0
        return 0

    def get_total_lessons(self, obj):
        return obj.lessons.count()

class PathSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Path
        fields = ['id', 'title', 'description', 'courses', 'image']

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'course', 'completed_lessons', 'is_course_complete']
        read_only_fields = ['user']


class LeaderboardSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user', 'points']

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email,
        }

class UserProfileSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email_reminders']

class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['goal', 'experience', 'preferred_style']

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'url', 'category', 'icon']


class MissionCompletionSerializer(serializers.ModelSerializer):
    goal_type = serializers.CharField(source="mission.goal_type")
    target = serializers.SerializerMethodField()

    class Meta:
        model = MissionCompletion
        fields = ["id", "mission", "goal_type", "target", "progress", "status"]

    def get_target(self, obj):
        return obj.mission.goal_reference.get('target', 100)


class MissionCompletionSerializer(serializers.ModelSerializer):
    goal_type = serializers.CharField(source="mission.goal_type")

    class Meta:
        model = MissionCompletion
        fields = [
            "id",
            "mission",
            "goal_type",  # Include goal_type in the response
            "progress",
            "status",
        ]

class SimulatedSavingsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatedSavingsAccount
        fields = ["id", "user", "balance"]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'type',
            'options',
            'explanation',
            'order'
        ]
        read_only_fields = ['id', 'created_at']

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['user', 'question', 'answer']
        read_only_fields = ['user']

class PathRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathRecommendation
        fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'name', 'description', 'cost', 'type', 'image', 'donation_organization']

class UserPurchaseSerializer(serializers.ModelSerializer):
    reward = RewardSerializer(read_only=True)

    class Meta:
        model = UserPurchase
        fields = ['id', 'reward', 'purchased_at']
        read_only_fields = ['reward', 'purchased_at']

    def create(self, validated_data):

        reward = validated_data.get('reward')
        return UserPurchase.objects.create(
            user=self.context['request'].user,
            reward=reward
        )

class BadgeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'image_url', 'criteria_type', 'threshold', 'badge_level']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return None

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ['badge', 'earned_at']

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    badges = UserBadgeSerializer(many=True, read_only=True, source='user.earned_badges')
    referral_code = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user", "email_reminders", "earned_money", "points", "profile_picture",
            "profile_avatar", "generated_images", "balance", "badges", "referral_code", "dark_mode"
        ]

    def get_balance(self, obj):
        return float(obj.earned_money)

class ReferralSerializer(serializers.ModelSerializer):
    referred_user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Referral
        fields = ['referred_user', 'created_at']

    def get_referred_user(self, obj):
        return {
            "id": obj.referred_user.id,
            "username": obj.referred_user.username
        }

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']

    def get_sender(self, obj):
        return {
            "id": obj.sender.id,
            "username": obj.sender.username
        }

    def get_receiver(self, obj):
        return {
            "id": obj.receiver.id,
            "username": obj.receiver.username
        }

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'type', 'question', 'exercise_data', 'category', 'difficulty']

class UserExerciseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExerciseProgress
        fields = ['exercise', 'completed', 'attempts', 'user_answer']
        read_only_fields = ['user']