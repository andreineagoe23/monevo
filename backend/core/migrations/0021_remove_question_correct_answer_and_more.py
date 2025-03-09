# Generated by Django 4.2 on 2025-03-09 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_question_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('knowledge_check', 'Knowledge Check'), ('preference_scale', 'Preference Scale'), ('budget_allocation', 'Budget Allocation')], max_length=20),
        ),
    ]
