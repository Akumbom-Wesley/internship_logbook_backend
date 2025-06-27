from django.urls import path
from apps.companies.views.admins import CompanyAdminInternshipRequestsView, ApproveRejectInternshipRequestView

urlpatterns = [
    path('requests/', CompanyAdminInternshipRequestsView.as_view(), name='company-admin-internship-requests'),
    path('requests/approve/<int:request_id>/', ApproveRejectInternshipRequestView.as_view(), name='approve-internship-request'),
]