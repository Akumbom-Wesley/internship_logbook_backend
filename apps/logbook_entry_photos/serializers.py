from rest_framework import serializers
from apps.logbook_entry_photos.models import LogbookEntryPhoto


class LogbookEntryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogbookEntryPhoto
        fields = ['id', 'photo', 'log_entry']