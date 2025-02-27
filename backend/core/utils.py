def check_and_award_badge(user, criteria_type):
    from .models import Badge, UserBadge, LessonCompletion, UserProgress, MissionCompletion
    badges = Badge.objects.filter(criteria_type=criteria_type, is_active=True)
    for badge in badges:
        if UserBadge.objects.filter(user=user, badge=badge).exists():
            continue
        
        earned = False
        if criteria_type == 'lessons_completed':
            count = LessonCompletion.objects.filter(user_progress__user=user).count()
            earned = count >= badge.threshold
        elif criteria_type == 'courses_completed':
            count = UserProgress.objects.filter(user=user, is_course_complete=True).count()
            earned = count >= badge.threshold
        elif criteria_type == 'streak_days':
            progress = UserProgress.objects.filter(user=user).order_by('-last_completed_date').first()
            earned = progress and progress.streak >= badge.threshold
        elif criteria_type == 'missions_completed':
            count = MissionCompletion.objects.filter(user=user, status='completed').count()
            earned = count >= badge.threshold
        
        if earned:
            UserBadge.objects.create(user=user, badge=badge)