# Generated by Django 4.2 on 2024-11-29 14:39

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_mission_mission_type_missioncompletion_completed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='detailed_content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
