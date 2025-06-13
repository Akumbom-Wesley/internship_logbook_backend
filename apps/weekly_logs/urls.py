from django.urls import path
from apps.weekly_logs.views import WeeklyLogListView, WeeklyLogDetailView, WeeklyLogCreateView, WeeklyLogUpdateView, WeeklyLogDeleteView

urlpatterns = [
    path('<int:logbook_id>/list', WeeklyLogListView.as_view(), name='weekly-log-list'),
    path('<int:weekly_log_id>/', WeeklyLogDetailView.as_view(), name='weekly-log-detail'),
    path('<int:logbook_id>/create/', WeeklyLogCreateView.as_view(), name='weekly-log-create'),
    path('<int:weekly_log_id>/<int:logbook_id>/update/', WeeklyLogUpdateView.as_view(), name='weekly-log-update'),
    path('<int:weekly_log_id>/delete/', WeeklyLogDeleteView.as_view(), name='weekly-log-delete'),
]