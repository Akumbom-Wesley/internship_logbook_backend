from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.students.views import StudentViewSet, CreateInternshipRequestView, StudentInternshipRequestsView, PendingInternshipRequestsView

# Define custom URL patterns first
urlpatterns = [
    path('requests/create/', CreateInternshipRequestView.as_view(), name='create-internship-request'),
    path('requests/', StudentInternshipRequestsView.as_view(), name='student-internship-requests'),
    path('requests/list', PendingInternshipRequestsView.as_view(), name='internship-request-list'),
]

router = DefaultRouter()
router.register(r'', StudentViewSet)

# Add router URLs to urlpatterns
urlpatterns += router.urls