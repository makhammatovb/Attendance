from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'groups'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Student(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')
    # attendance = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    date = models.DateField(default=date.today)
    present = models.BooleanField(default=False)
    time = models.TimeField(default=timezone.now, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='attendances')

    def __str__(self):
        return f'{self.student.name} - {self.date}'

    class Meta:
        unique_together = ('student', 'date')
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'


class Salary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    paid_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='salaries')

    def __str__(self):
        return f'{self.student.name} - {self.paid_date}'

    class Meta:
        db_table = 'salary'
        verbose_name = 'Salary'
        verbose_name_plural = 'Salaries'
