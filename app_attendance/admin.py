from django.contrib import admin
from .models import Students, Attendance, Salary


# Register your models here.
@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age', 'phone')
    search_fields = ('name', 'surname', 'phone')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'present')
    list_filter = ('date', 'present')
    search_fields = ('student__name', 'date')

@admin.action(description='Mark salaries as paid')
def mark_as_paid(modeladmin, request, queryset):
    queryset.update(is_paid=True)

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'paid_date', 'is_paid')
    list_filter = ('is_paid', 'paid_date')
    search_fields = ('student__name', 'amount')
    actions = [mark_as_paid]


