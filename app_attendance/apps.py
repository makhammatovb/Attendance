from django.apps import AppConfig


class AppAttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_attendance'

    # def ready(self):
    #     import app_attendance.signals
