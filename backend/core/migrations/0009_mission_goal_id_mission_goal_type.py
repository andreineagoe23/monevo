# Generated by Django 5.1.4 on 2025-01-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_mission_mission_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='goal_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='goal_type',
            field=models.CharField(choices=[('complete_lesson', 'Complete Lesson'), ('complete_exercise', 'Complete Exercise'), ('complete_course', 'Complete Course')], default='complete_lesson', max_length=50),
        ),
    ]
