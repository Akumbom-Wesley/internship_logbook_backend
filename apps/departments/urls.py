from django.urls import path
from apps.departments.views import DepartmentListCreateView, DepartmentDetailView

urlpatterns = [
    path('list/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
]
