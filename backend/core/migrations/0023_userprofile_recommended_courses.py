# Generated by Django 4.2 on 2025-03-09 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_course_options_course_is_active_course_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='recommended_courses',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
