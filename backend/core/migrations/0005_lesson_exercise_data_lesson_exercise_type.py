# Generated by Django 5.1.4 on 2025-01-02 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_userprofile_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='exercise_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='exercise_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]