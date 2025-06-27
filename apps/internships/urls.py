from django.urls import path
from apps.internships.views import (
    InternshipListView, InternshipDetailView, InternshipUpdateView,
    InternshipDeleteView, InternshipBulkUpdateView,
    InternshipMyListView, OngoingInternshipView, InternshipReportDownloadView
)
from apps.utils.internship_report import InternshipReportGenerateView

urlpatterns = [
    path('<int:company_id>/list', InternshipListView.as_view(), name='internship-list'),
    path('list', InternshipMyListView.as_view(), name='internships-by-student'),
    path('<int:internship_id>/', InternshipDetailView.as_view(), name='internship-detail'),
    path('ongoing/', OngoingInternshipView.as_view(), name='student-ongoing-internship'),
    path('<int:internship_id>/update/', InternshipUpdateView.as_view(), name='internship-update'),
    path('<int:internship_id>/delete/', InternshipDeleteView.as_view(), name='internship-delete'),
    path('<int:company_id>/bulk-update/', InternshipBulkUpdateView.as_view(), name='internship-bulk-update'),
    path('<int:internship_id>/report/', InternshipReportDownloadView.as_view(), name='internship-report'),
    path('<int:internship_id>/generate-report/', InternshipReportGenerateView.as_view(), name='generate-internship-report'),
]