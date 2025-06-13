from django.urls import path
from apps.logbook_entries.views import (LogbookEntryListView, LogbookEntryDetailView, LogbookEntryCreateView,
                        LogbookEntryUpdateView, LogbookEntryDeleteView, LogbookEntryApproveView)

urlpatterns = [
    path('<int:entry_id>/', LogbookEntryDetailView.as_view(), name='logbook-entry-detail'),
    path('<int:weekly_log_id>/list/', LogbookEntryListView.as_view(), name='logbook-entry-detail-by-week'),
    path('add/', LogbookEntryCreateView.as_view(), name='logbook-entry-create'),
    path('<int:entry_id>/update/', LogbookEntryUpdateView.as_view(), name='logbook-entry-update'),
    path('<int:entry_id>/delete/', LogbookEntryDeleteView.as_view(), name='logbook-entry-delete'),
    path('<int:entry_id>/approve/', LogbookEntryApproveView.as_view(), name='logbook-entry-approve'),
]