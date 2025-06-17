from django.urls import path
from apps.companies.views.companies import (
    CompanyCreateView,
    CompanyListView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView,
)

urlpatterns = [
    path('list', CompanyListView.as_view(), name='company-list'),
    path('create/', CompanyCreateView.as_view(), name='company-create'),
    path('<int:pk>', CompanyDetailView.as_view(), name='company-detail'),
    path('<int:pk>/update/', CompanyUpdateView.as_view(), name='company-update'),
    path('<int:pk>/delete/', CompanyDeleteView.as_view(), name='company-delete'),
]
