from django.urls import path
from apps.supervisors.views import SupervisorAssignedInternshipsView

urlpatterns = [
    path('assigned-internships/', SupervisorAssignedInternshipsView.as_view(), name='supervisor-assigned-internships'),
]