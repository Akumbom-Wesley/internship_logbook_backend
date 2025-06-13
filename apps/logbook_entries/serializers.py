from rest_framework import serializers
from apps.logbook_entries.models import LogbookEntry
from apps.logbook_entry_photos.models import LogbookEntryPhoto
from apps.logbook_entry_photos.serializers import LogbookEntryPhotoSerializer
from django.conf import settings


class LogbookEntrySerializer(serializers.ModelSerializer):
    photos = LogbookEntryPhotoSerializer(many=True, required=False)

    class Meta:
        model = LogbookEntry
        fields = ['id', 'description', 'is_immutable', 'feedback', 'weekly_log', 'photos']

    def create(self, validated_data):
        request = self.context.get("request")
        photos = request.FILES.getlist("photos")
        instance = LogbookEntry(**validated_data)
        # instance.save() will sign automatically
        instance.save()
        for photo in photos:
            LogbookEntryPhoto.objects.create(log_entry=instance, photo=photo)
        return instance

    def update(self, instance, validated_data):
        if instance.is_immutable:
            raise serializers.ValidationError("Cannot update an already approved log entry.")

        request = self.context.get("request")
        photos = request.FILES.getlist("photos")

        # Update fields, then regenerate signature
        if request.user.role == 'student':
            if 'description' in validated_data:
                instance.description = validated_data['description']
        elif request.user.role == 'supervisor':
            if 'feedback' in validated_data:
                instance.feedback = validated_data['feedback']

        # Regenerate signature using server-managed key
        student = instance.weekly_log.logbook.internship.student
        try:
            private_key_hex = student.get_private_key()
            instance.signature = instance.generate_signature(private_key_hex)
        except Exception as e:
            raise serializers.ValidationError(f"Failed to regenerate signature: {e}")

        instance.save()
        # Append new photos if any
        for photo in photos:
            LogbookEntryPhoto.objects.create(log_entry=instance, photo=photo)
        return instance

    def validate(self, data):
        # e.g., enforce max 5 entries per week, weekday rules, etc.
        # This part remains as before, using instance.weekly_log when updating.
        weekly_log = data.get('weekly_log') or getattr(self.instance, 'weekly_log', None)
        if not weekly_log:
            raise serializers.ValidationError("Weekly log must be provided.")
        if not self.instance and LogbookEntry.objects.filter(weekly_log=weekly_log).count() >= 5:
            raise serializers.ValidationError("Cannot add more than 5 log entries per week.")
        # ... weekday and period checks ...
        return data