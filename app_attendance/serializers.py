from rest_framework import serializers
from .models import Group, Student, Attendance, Salary

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_surname = serializers.CharField(source='student.surname', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    attendances = AttendanceSerializer(many=True, read_only=True)
    salaries = SalarySerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
