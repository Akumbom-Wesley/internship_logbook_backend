from django.urls import path
from .views import EvaluationCreateView, EvaluationPDFDownloadView

urlpatterns = [
    path('<int:internship_id>/create/', EvaluationCreateView.as_view(), name='create_evaluation'),
    path('<int:internship_id>/download/', EvaluationPDFDownloadView.as_view(), name='download_evaluation')
]