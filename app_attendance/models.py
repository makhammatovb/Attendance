from django.db import models


# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Attendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    time = models.TimeField(null=True, blank=True)

    def clean(self):
        if not self.present and self.time:
            raise ValidationError("Time cannot be set if the student is not present.")

    def __str__(self):
        return f'{self.student.name} - {self.date}'

    class Meta:
        unique_together = ('student', 'date')
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'


class Salary(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    paid_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student.name} - {self.paid_date}'

    class Meta:
        db_table = 'salary'
        verbose_name = 'Salary'
        verbose_name_plural = 'Salaries'