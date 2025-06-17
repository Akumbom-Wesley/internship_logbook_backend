from django.urls import path
from apps.internships.views import (
    InternshipListView, InternshipDetailView, InternshipUpdateView,
    InternshipDeleteView, InternshipBulkUpdateView,
     InternshipMyListView
)

urlpatterns = [
    path('<int:company_id>/list', InternshipListView.as_view(), name='internship-list'),
    path('list', InternshipMyListView.as_view(), name='internships-by-student'),
    path('<int:internship_id>/', InternshipDetailView.as_view(), name='internship-detail'),
    path('<int:internship_id>/update/', InternshipUpdateView.as_view(), name='internship-update'),
    path('<int:internship_id>/delete/', InternshipDeleteView.as_view(), name='internship-delete'),
    path('<int:company_id>/bulk-update/', InternshipBulkUpdateView.as_view(), name='internship-bulk-update'),
]