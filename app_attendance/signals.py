from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Group, Student, Attendance
from datetime import date, time

@receiver(post_save, sender=Group)
def create_or_update_student_attendance(sender, instance, created, **kwargs):
    if created:
        update_student_attendance(instance)

def update_student_attendance(group):
    students = group.students.all()
    for student in students:
        attendance, created = Attendance.objects.get_or_create(
            student=student,
            date=date.today(),
            defaults={
                'present': None,
                'time': None
            }
        )
        if not created:
            attendance.present = None
            attendance.time = None
            attendance.save()