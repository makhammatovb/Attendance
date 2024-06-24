# Generated by Django 5.0.4 on 2024-06-23 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_attendance', '0005_remove_student_attendance_alter_attendance_present_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='app_attendance.group'),
            preserve_default=False,
        ),
    ]
