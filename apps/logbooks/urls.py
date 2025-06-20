from django.urls import path
from apps.logbooks.views import LogbookListView, LogbookDetailView, LogbookCreateView, LogbookUpdateView, LogbookDeleteView

urlpatterns = [
    path('<int:internship_id>/list', LogbookListView.as_view(), name='logbook-list'),
    path('<int:logbook_id>/', LogbookDetailView.as_view(), name='logbook-detail'),
    path('create/', LogbookCreateView.as_view(), name='logbook-create'),
    path('<int:logbook_id>/update/', LogbookUpdateView.as_view(), name='logbook-update'),
    path('<int:logbook_id>/delete/', LogbookDeleteView.as_view(), name='logbook-delete'),
]