from django.urls import path
from apps.logbook_entry_photos.views import LogbookEntryPhotoListView, LogbookEntryPhotoDetailView, LogbookEntryPhotoCreateView, LogbookEntryPhotoUpdateView, LogbookEntryPhotoDeleteView

urlpatterns = [
    path('list', LogbookEntryPhotoListView.as_view(), name='logbook-entry-photo-list'),
    path('<int:photo_id>/', LogbookEntryPhotoDetailView.as_view(), name='logbook-entry-photo-detail'),
    path('upload/', LogbookEntryPhotoCreateView.as_view(), name='logbook-entry-photo-create'),
    path('<int:photo_id>/update/', LogbookEntryPhotoUpdateView.as_view(), name='logbook-entry-photo-update'),
    path('<int:photo_id>/delete/', LogbookEntryPhotoDeleteView.as_view(), name='logbook-entry-photo-delete'),
]