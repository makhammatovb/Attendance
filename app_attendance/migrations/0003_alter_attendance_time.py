# Generated by Django 5.0.4 on 2024-06-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_attendance', '0002_alter_attendance_options_alter_salary_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
