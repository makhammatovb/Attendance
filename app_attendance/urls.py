from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, StudentViewSet, AttendanceViewSet, SalaryViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'students', StudentViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'salaries', SalaryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
