from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Path,
    Course,
    Lesson,
    Quiz,
    UserProfile,
    UserProgress,
    Mission,
    MissionCompletion,
    SimulatedSavingsAccount,
    Question,
    Reward,
    Badge,
    UserBadge,
    Referral,
    Exercise,
    UserExerciseProgress,
    LessonSection,
    PollResponse,
    FinanceFact,
    UserFactProgress,
    FAQ,
    ContactMessage
)

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Admin configuration for managing referrals."""
    list_display = ('referrer', 'referred_user', 'created_at')

@admin.register(PollResponse)
class PollResponseAdmin(admin.ModelAdmin):
    """Admin configuration for managing poll responses."""
    list_display = ('question', 'answer', 'responded_at')
    list_filter = ('question',)

class LessonSectionInline(admin.TabularInline):
    """Inline configuration for managing lesson sections."""
    model = LessonSection
    extra = 1
    fieldsets = [
        (None, {
            'fields': ('order', 'title', 'content_type')
        }),
        ('Text Content', {
            'fields': ('text_content',),
            'classes': ('collapse',),
        }),
        ('Video Content', {
            'fields': ('video_url',),
            'classes': ('collapse',),
        }),
        ('Exercise Content', {
            'fields': ('exercise_type', 'exercise_data'),
            'classes': ('collapse',),
            'description': """
                <strong>Exercise Data Format:</strong>
                <ul>
                    <li><strong>Multiple Choice:</strong> 
                        <pre>{
                        "question": "Your question here",
                        "options": ["Option 1", "Option 2", "Option 3"],
                        "correctAnswer": 0 
                        }</pre>
                    </li>
                    <li><strong>Budget Allocation:</strong> 
                        <pre>{
  "question": "Allocate the budget",
  "categories": ["Category 1", "Category 2"],
  "total": 1000 
}</pre>
                    </li>
                </ul>
            """,
        }),
    ]

class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for managing lessons."""
    inlines = [LessonSectionInline]
    list_display = ('title', 'course', 'section_count')
    
    def section_count(self, obj):
        """Return the count of sections in a lesson."""
        return obj.sections.count()

class MissionAdmin(admin.ModelAdmin):
    """Admin configuration for managing missions."""
    list_display = ('name', 'mission_type', 'goal_type', 'points_reward')
    fields = ('name', 'description', 'points_reward', 'mission_type', 'goal_type', 'goal_reference')
    list_filter = ('mission_type', 'goal_type')
    search_fields = ('name', 'description')

    def goal_target(self, obj):
        """Determine the goal target based on mission type and goal type."""
        if obj.goal_type == "read_fact":
            return "1 Fact" if obj.mission_type == "daily" else "5 Facts"
        return obj.goal_reference

class MissionCompletionAdmin(admin.ModelAdmin):
    """Admin configuration for managing mission completions."""
    list_display = ('user', 'mission', 'progress', 'status', 'completed_at')
    fields = ('user', 'mission', 'progress', 'status', 'completed_at')
    list_filter = ('status', 'mission__mission_type')
    search_fields = ('user__username', 'mission__name')

class SimulatedSavingsAccountAdmin(admin.ModelAdmin):
    """Admin configuration for managing simulated savings accounts."""
    list_display = ('user', 'balance')
    fields = ('user', 'balance')
    search_fields = ('user__username',)

class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for managing questions."""
    list_display = ('text', 'type', 'order', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('text',)

class RewardAdmin(admin.ModelAdmin):
    """Admin configuration for managing rewards."""
    list_display = ('name', 'type', 'cost', 'is_active')
    list_filter = ('type', 'is_active')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'cost', 'type', 'image', 'is_active')}),
        ('Donation Specific', {
            'fields': ('donation_organization',),
            'classes': ('collapse',),
            'description': 'Only fill for donation causes'
        }),
    )

class BadgeAdmin(admin.ModelAdmin):
    """Admin configuration for managing badges."""
    list_display = ('name', 'badge_level', 'criteria_type', 'threshold', 'is_active', 'badge_image')
    fields = ('name', 'description', 'image', 'criteria_type', 'threshold', 'badge_level', 'is_active')
    list_filter = ('badge_level', 'criteria_type', 'is_active')
    search_fields = ('name', 'criteria_type')

    def badge_image(self, obj):
        """Display the badge image in the admin interface."""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "No Image"

    badge_image.allow_tags = True
    badge_image.short_description = "Badge Image"

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Admin configuration for managing exercises."""
    list_display = ('type', 'category', 'difficulty', 'created_at')
    list_filter = ('type', 'category', 'difficulty')
    search_fields = ('question', 'category')

@admin.register(UserExerciseProgress)
class UserExerciseProgressAdmin(admin.ModelAdmin):
    """Admin configuration for managing user exercise progress."""
    list_display = ('user', 'exercise', 'completed', 'attempts')
    list_filter = ('completed', 'exercise__type')
    search_fields = ('user__username', 'exercise__question')

@admin.register(FinanceFact)
class FinanceFactAdmin(admin.ModelAdmin):
    """Admin configuration for managing finance facts."""
    list_display = ('text', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('text',)
    list_editable = ('is_active',)

@admin.register(UserFactProgress)
class UserFactProgressAdmin(admin.ModelAdmin):
    """Admin configuration for managing user fact progress."""
    list_display = ('user', 'fact', 'read_at')
    list_filter = ('read_at',)
    search_fields = ('user__username', 'fact__text')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for managing user profiles."""
    list_display = ('user', 'earned_money', 'points', 'referral_code', 'has_paid', 'dark_mode', 'email_reminder_preference', 'streak')
    list_filter = ('has_paid', 'dark_mode', 'email_reminder_preference')
    search_fields = ('user__username', 'user__email', 'referral_code')
    readonly_fields = ('earned_money', 'points', 'referral_points', 'streak')

admin.site.register(Badge, BadgeAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Path)
admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(UserProgress)
admin.site.register(Mission, MissionAdmin)
admin.site.register(MissionCompletion, MissionCompletionAdmin)
admin.site.register(SimulatedSavingsAccount, SimulatedSavingsAccountAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(FAQ)
admin.site.register(ContactMessage)