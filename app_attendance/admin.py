from django import forms
from django.contrib import admin
from django.utils import timezone
from .models import Group, Student, Attendance, Salary
from datetime import date
from django.forms import BaseInlineFormSet


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            for student in self.instance.students.all():
                field_name = f'attendance_{student.id}_present'
                self.fields[field_name] = forms.BooleanField(
                    required=False,
                    initial=self.get_initial_attendance(student),
                    label=f'{student.name} {student.surname}'
                )

    def get_initial_attendance(self, student):
        today = date.today()
        attendance = Attendance.objects.filter(student=student, date=today).first()
        return attendance.present if attendance else False

    def save(self, commit=True):
        group = super().save(commit=commit)
        if not group.pk:
            group.save()

        for student in group.students.all():
            field_name = f'attendance_{student.id}_present'
            present = self.cleaned_data.get(field_name, False)
            if present:
                Attendance.objects.create(
                    student=student,
                    date=date.today(),
                    present=True,
                    time=timezone.now().time(),
                    group=group
                )
        return group

class StudentInline(admin.TabularInline):
    model = Student
    fields = ('name', 'surname', 'phone')
    readonly_fields = ('name', 'surname', 'phone')
    extra = 0


class BaseAttendanceInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and isinstance(self.instance, Group):
            self.queryset = Attendance.objects.filter(group=self.instance)

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    fields = ('student_name', 'student_surname', 'date', 'time', 'present')
    readonly_fields = ('student_name', 'student_surname')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        group_id = request.resolver_match.kwargs.get('object_id')
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
                today = date.today()
                students = group.students.all()

                for student in students:
                    if not Attendance.objects.filter(student=student, date=today).exists():
                        Attendance.objects.create(student=student, date=today, group=group)

                qs = Attendance.objects.filter(student__group_id=group_id, date=today)
            except Group.DoesNotExist:
                qs = Attendance.objects.none()
        return qs

    def student_name(self, instance):
        return instance.student.name

    def student_surname(self, instance):
        return instance.student.surname

    student_name.short_description = 'Name'
    student_surname.short_description = 'Surname'


class SalaryInline(admin.TabularInline):
    model = Salary
    fields = ('student', 'amount', 'paid_date', 'is_paid')
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['paid_date'].initial = date.today()
        return formset


def mark_present(modeladmin, request, queryset):
    for student in queryset:
        Attendance.objects.create(
            student=student,
            date=date.today(),
            present=True,
            time=timezone.now().time(),
        )

mark_present.short_description = "Mark selected students as present"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age', 'email', 'phone', 'group')
    list_filter = ('group',)
    search_fields = ('name', 'surname', 'group__name')
    inlines = [SalaryInline]
    actions = [mark_present]

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'present', 'time', 'group')
    list_filter = ('date', 'present', 'student__group')
    search_fields = ('student__name', 'student__surname')
    ordering = ('-date',)

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'paid_date', 'is_paid')
    list_filter = ('paid_date', 'is_paid', 'student__group')
    search_fields = ('student__name', 'student__surname')
    ordering = ('-paid_date',)


class StudentAttendanceInline(admin.TabularInline):
    model = Student
    fields = ('name', 'surname', 'phone')
    readonly_fields = ('name', 'surname')
    extra = 0
    can_delete = False

    def attendance_status(self, instance):
        today = date.today()
        attendance = Attendance.objects.filter(student=instance, date=today).first()
        if attendance:
            return "Present" if attendance.present else "Not Present"
        return "Not Marked"

    attendance_status.short_description = 'Attendance Status'

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    list_display = ('name',)
    inlines = [StudentInline, AttendanceInline, SalaryInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('students')
