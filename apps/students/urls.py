from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.students.views import StudentViewSet, CreateInternshipRequestView, StudentInternshipRequestsView

router = DefaultRouter()
router.register(r'', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('requests/create/', CreateInternshipRequestView.as_view(), name='create-internship-request'),
    path('requests/', StudentInternshipRequestsView.as_view(), name='student-internship-requests'),
]