# Generated by Django 5.1.1 on 2025-05-02 13:39

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='badges/')),
                ('criteria_type', models.CharField(choices=[('lessons_completed', 'Lessons Completed'), ('courses_completed', 'Courses Completed'), ('streak_days', 'Streak Days'), ('points_earned', 'Points Earned'), ('missions_completed', 'Missions Completed'), ('savings_balance', 'Savings Balance')], max_length=50)),
                ('threshold', models.IntegerField()),
                ('badge_level', models.CharField(choices=[('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')], default='bronze', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='course_images/')),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('drag-and-drop', 'Drag and Drop'), ('multiple-choice', 'Multiple Choice'), ('budget-allocation', 'Budget Allocation')], max_length=50)),
                ('question', models.TextField()),
                ('exercise_data', models.JSONField(help_text='Structured data based on exercise type')),
                ('correct_answer', models.JSONField(help_text='Correct answer structure')),
                ('category', models.CharField(default='General', max_length=100)),
                ('difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinanceFact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('category', models.CharField(default='General', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='path_images/')),
            ],
            options={
                'verbose_name': 'Path',
                'verbose_name_plural': 'Paths',
            },
        ),
        migrations.CreateModel(
            name='PathRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('criteria', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('type', models.CharField(choices=[('knowledge_check', 'Knowledge Check'), ('preference_scale', 'Preference Scale'), ('budget_allocation', 'Budget Allocation')], max_length=20)),
                ('options', models.JSONField()),
                ('explanation', models.TextField(blank=True, null=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.CharField(default='General', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(choices=[('shop', 'Shop Item'), ('donate', 'Donation Cause')], max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='rewards/')),
                ('is_active', models.BooleanField(default=True)),
                ('donation_organization', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('basic_finance', 'Basic Finance'), ('real_estate', 'Real Estate'), ('crypto', 'Crypto'), ('forex', 'Forex')], max_length=50)),
                ('url', models.URLField(blank=True, null=True)),
                ('icon', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('short_description', models.TextField(blank=True)),
                ('detailed_content', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='lesson_images/')),
                ('video_url', models.URLField(blank=True, null=True)),
                ('exercise_type', models.CharField(blank=True, choices=[('drag-and-drop', 'Drag and Drop'), ('multiple-choice', 'Multiple Choice'), ('quiz', 'Quiz')], max_length=50, null=True)),
                ('exercise_data', models.JSONField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='core.course')),
            ],
            options={
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
            },
        ),
        migrations.CreateModel(
            name='LessonCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='LessonSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=200)),
                ('content_type', models.CharField(choices=[('text', 'Text Content'), ('video', 'Video'), ('exercise', 'Interactive Exercise')], default='text', max_length=20)),
                ('text_content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('exercise_type', models.CharField(blank=True, choices=[('drag-and-drop', 'Drag and Drop'), ('multiple-choice', 'Multiple Choice'), ('budget-allocation', 'Budget Allocation')], max_length=50, null=True)),
                ('exercise_data', models.JSONField(blank=True, null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='core.lesson')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('lesson', 'order')},
            },
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('points_reward', models.IntegerField()),
                ('mission_type', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly')], default='daily', max_length=10)),
                ('goal_type', models.CharField(choices=[('complete_lesson', 'Complete Lesson'), ('add_savings', 'Add Savings'), ('read_fact', 'Read Finance Fact'), ('complete_path', 'Complete Path')], default='complete_lesson', max_length=50)),
                ('goal_reference', models.JSONField(blank=True, null=True)),
                ('fact', models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.financefact')),
            ],
        ),
        migrations.CreateModel(
            name='MissionCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='not_started', max_length=20)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completions', to='core.mission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mission_completions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='path',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='core.path'),
        ),
        migrations.CreateModel(
            name='PollResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
                ('responded_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.question')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.CharField(blank=True, max_length=255, null=True)),
                ('experience', models.CharField(blank=True, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], max_length=50, null=True)),
                ('preferred_style', models.CharField(blank=True, choices=[('Visual', 'Visual'), ('Auditory', 'Auditory'), ('Kinesthetic', 'Kinesthetic')], max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('question', models.TextField()),
                ('choices', models.JSONField()),
                ('correct_answer', models.CharField(max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='core.course')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('referred_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='referral_received', to=settings.AUTH_USER_MODEL)),
                ('referrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals_made', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SectionCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.lessonsection')),
            ],
        ),
        migrations.CreateModel(
            name='SimulatedSavingsAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StripePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_payment_id', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='GBP', max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned_money', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('points', models.PositiveIntegerField(default=0)),
                ('profile_avatar', models.URLField(blank=True, null=True)),
                ('recommended_courses', models.JSONField(blank=True, default=list)),
                ('referral_code', models.CharField(max_length=20, null=True, unique=True)),
                ('referral_points', models.PositiveIntegerField(default=0)),
                ('dark_mode', models.BooleanField(default=False)),
                ('has_paid', models.BooleanField(default=False)),
                ('stripe_payment_id', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('email_reminders', models.BooleanField(default=True)),
                ('email_frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily', max_length=10)),
                ('streak', models.PositiveIntegerField(default=0)),
                ('last_completed_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_course_complete', models.BooleanField(default=False)),
                ('is_questionnaire_completed', models.BooleanField(default=False)),
                ('course_completed_at', models.DateTimeField(blank=True, null=True)),
                ('completed_lessons', models.ManyToManyField(blank=True, through='core.LessonCompletion', to='core.lesson')),
                ('completed_sections', models.ManyToManyField(blank=True, through='core.SectionCompletion', to='core.lessonsection')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress_courses', to='core.course')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_progress', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Progress',
                'verbose_name_plural': 'User Progress',
            },
        ),
        migrations.AddField(
            model_name='sectioncompletion',
            name='user_progress',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprogress'),
        ),
        migrations.AddField(
            model_name='lessoncompletion',
            name='user_progress',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprogress'),
        ),
        migrations.CreateModel(
            name='UserPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_at', models.DateTimeField(auto_now_add=True)),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.question')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_responses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('sender', 'receiver')},
            },
        ),
        migrations.CreateModel(
            name='ExerciseCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('attempts', models.PositiveIntegerField(default=0)),
                ('user_answer', models.JSONField(blank=True, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.lessonsection')),
            ],
            options={
                'unique_together': {('user', 'exercise', 'section')},
            },
        ),
        migrations.CreateModel(
            name='QuizCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'quiz')},
            },
        ),
        migrations.CreateModel(
            name='UserBadge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.badge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='earned_badges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'badge')},
            },
        ),
        migrations.CreateModel(
            name='UserExerciseProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('attempts', models.PositiveIntegerField(default=0)),
                ('last_attempt', models.DateTimeField(auto_now=True)),
                ('user_answer', models.JSONField(blank=True, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'exercise')},
            },
        ),
        migrations.CreateModel(
            name='UserFactProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_at', models.DateTimeField(auto_now_add=True)),
                ('fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.financefact')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'fact')},
            },
        ),
    ]
