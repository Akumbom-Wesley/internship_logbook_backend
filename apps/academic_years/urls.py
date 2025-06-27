from django.urls import path
from .views import ListAcademicYearView

urlpatterns = [
    path('list', ListAcademicYearView.as_view(), name='list'),
]