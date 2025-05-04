from django.urls import path
from apps.companies.views.admins import CompanyAdminInternshipRequestsView, ApproveInternshipRequestView

urlpatterns = [
    path('requests/', CompanyAdminInternshipRequestsView.as_view(), name='company-admin-internship-requests'),
    path('requests/approve/<int:request_id>/', ApproveInternshipRequestView.as_view(), name='approve-internship-request'),
]