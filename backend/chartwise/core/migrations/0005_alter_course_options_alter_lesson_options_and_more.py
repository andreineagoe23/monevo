# Generated by Django 5.1.2 on 2024-11-06 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_path_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Course', 'verbose_name_plural': 'Courses'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'Lesson', 'verbose_name_plural': 'Lessons'},
        ),
        migrations.AlterModelOptions(
            name='path',
            options={'verbose_name': 'Path', 'verbose_name_plural': 'Paths'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name': 'Quiz', 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User Profile', 'verbose_name_plural': 'User Profiles'},
        ),
        migrations.AlterModelOptions(
            name='userprogress',
            options={'verbose_name': 'User Progress', 'verbose_name_plural': 'User Progress'},
        ),
    ]
