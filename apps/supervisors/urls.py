from django.urls import path
from apps.supervisors.views import (
    SupervisorAssignedInternshipsView, SupervisorAssignedStudentsView, SupervisorStudentLogActivityView
)

urlpatterns = [
    path('assigned-internships/', SupervisorAssignedInternshipsView.as_view(), name='supervisor-assigned-internships'),
    path('assigned-students/', SupervisorAssignedStudentsView.as_view(), name='supervisor-assigned-students'),
    path('assigned-students/activity/', SupervisorStudentLogActivityView.as_view(), name='supervisor-log-activity'),

]