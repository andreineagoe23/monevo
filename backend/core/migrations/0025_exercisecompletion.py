# Generated by Django 4.2 on 2025-03-15 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0024_financefact_mission_fact_userfactprogress'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('attempts', models.PositiveIntegerField(default=0)),
                ('user_answer', models.JSONField(blank=True, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.exercise')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.lessonsection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'exercise', 'section')},
            },
        ),
    ]
