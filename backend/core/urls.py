from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    CustomTokenRefreshView,
    UserProfileViewSet,
    CourseViewSet,
    LessonViewSet,
    QuizViewSet,
    PathViewSet,
    RegisterView,
    UserProgressViewSet,
    LeaderboardViewSet,
    UserSettingsView,
    UserProfileView,
    MissionView,
    QuestionnaireView,
    ChatbotView,
    ToolListView,
    SavingsGoalCalculatorView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    SavingsAccountView,
    FinanceFactView,
    RecommendationView,
    QuestionnaireSubmitView,
    PersonalizedPathView,
    get_exercise_progress,
    RecentActivityView,
    RewardViewSet,
    UserPurchaseViewSet,
    get_csrf_token,
    UserBadgeViewSet,
    BadgeViewSet,
    update_avatar,
    ReferralView,
    UserSearchView,
    FriendRequestView,
    FriendsLeaderboardView,
    UserExerciseProgressViewSet,
    ExerciseViewSet,
    EnhancedQuestionnaireView,
    complete_exercise,
    reset_exercise,
    TokenObtainPairView,
    StripeWebhookView,
    VerifySessionView,
    HuggingFaceProxyView,
    LoginSecureView,
    RegisterSecureView,
    LogoutSecureView,
    VerifyAuthView,
    OpenRouterProxyView,
    contact_us,
    FAQListView,
    vote_faq,
    delete_account,
    UserRankView,
    PortfolioViewSet,
    FinancialGoalViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from core.views import CustomTokenObtainPairView, LogoutView

router = DefaultRouter()
router.register(r'userprogress', UserProgressViewSet, basename='userprogress')
router.register(r'userprofiles', UserProfileViewSet, basename='userprofile')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'paths', PathViewSet, basename='path')
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'user-badges', UserBadgeViewSet, basename='userbadge')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'exercise-progress', UserExerciseProgressViewSet, basename='exercise-progress')
router.register(r'friend-requests', FriendRequestView, basename='friend-request')
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')
router.register(r'financial-goals', FinancialGoalViewSet, basename='financial-goals')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),

    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('login-secure/', LoginSecureView.as_view(), name='login-secure'),
    path('register-secure/', RegisterSecureView.as_view(), name='register-secure'),
    path('logout-secure/', LogoutSecureView.as_view(), name='logout-secure'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('verify-auth/', VerifyAuthView.as_view(), name='verify-auth'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('progress/complete/', UserProgressViewSet.as_view({'post': 'complete'}), name='progress-complete'),
    path('userprofiles/update/', UserProfileViewSet.as_view({'put': 'update_profile'}), name='update-profile'),

    path("userprofile/", UserProfileView.as_view(), name="userprofile"),
    path("userprofiles/", include(router.urls)),
    path('update-avatar/', views.update_avatar, name='update_avatar'),

    path('leaderboard/', LeaderboardViewSet.as_view(), name='leaderboard'),
    path('leaderboard/rank/', UserRankView.as_view(), name='user-rank'),
    path('user/settings/', UserSettingsView.as_view(), name='user-settings'),

    path("missions/", MissionView.as_view(), name="missions"),
    path("missions/<int:mission_id>/update/", MissionView.as_view(), name="mission-update"),
    path("savings-account/", SavingsAccountView.as_view(), name="savings-account"),
    path("finance-fact/", FinanceFactView.as_view(), name="finance-fact"),

    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('recommendation/<int:user_id>/', RecommendationView.as_view(), name='recommendation'),
    path('enhanced-questionnaire/submit/', EnhancedQuestionnaireView.as_view(), name='enhanced-questionnaire-submit'),
    path('enhanced-questionnaire/', EnhancedQuestionnaireView.as_view(), name='enhanced-questionnaire'),
    path('personalized-path/', PersonalizedPathView.as_view(), name='personalized-path'),

    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('verify-session/', VerifySessionView.as_view(), name='verify-session'),

    path('exercises/complete/', complete_exercise, name='complete-exercise'),
    path('exercises/reset/', reset_exercise, name='reset-exercise'),


    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('chatbot/webhook/', ChatbotView.dialogflow_webhook, name='chatbot-webhook'),

    path('tools/', ToolListView.as_view(), name='tool-list'),
    path('calculate-savings-goal/', SavingsGoalCalculatorView.as_view(), name='calculate_savings_goal'),

    path('exercises/progress/<int:exercise_id>/', get_exercise_progress, name='exercise-progress'),
    path('recent-activity/', RecentActivityView.as_view(), name='recent-activity'),

    path('rewards/shop/', RewardViewSet.as_view({'get': 'list'}), {'type': 'shop'}, name='shop-rewards'),
    path('rewards/donate/', RewardViewSet.as_view({'get': 'list'}), {'type': 'donate'}, name='donate-rewards'),
    path('purchases/', UserPurchaseViewSet.as_view({'post': 'create'}), name='purchases-create'),

    path('referrals/', ReferralView.as_view(), name='referrals'),
    path('search-users/', UserSearchView.as_view(), name='user-search'),
    path('leaderboard/friends/', FriendsLeaderboardView.as_view(), name='friends-leaderboard'),

    path('proxy/hf/', HuggingFaceProxyView.as_view(), name='hf-proxy'),
    path('proxy/openrouter/', OpenRouterProxyView.as_view(), name='openrouter-proxy'),
    path('change-password/', views.change_password, name='change-password'),
    path('delete-account/', delete_account, name='delete-account'),
    path('contact/', contact_us, name='contact-us'),

    path('faq/', FAQListView.as_view(), name='faq-list'),
    path('faq/<int:faq_id>/vote/', vote_faq, name='faq-vote'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)