# Generated by Django 4.2 on 2025-02-12 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_userprogress_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='goal_type',
            field=models.CharField(choices=[('complete_lesson', 'Complete Lesson'), ('add_savings', 'Add Savings'), ('read_fact', 'Read Finance Fact'), ('complete_path', 'Complete Path')], default='complete_lesson', max_length=50),
        ),
    ]
