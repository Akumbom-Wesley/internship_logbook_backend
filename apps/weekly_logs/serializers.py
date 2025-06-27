from rest_framework import serializers
from apps.weekly_logs.models import WeeklyLog
from apps.logbook_entries.models import LogbookEntry
from django.utils import timezone


class WeeklyLogSerializer(serializers.ModelSerializer):
    logbook_entries = serializers.SerializerMethodField()
    week_start_date = serializers.ReadOnlyField()
    week_end_date = serializers.ReadOnlyField()

    class Meta:
        model = WeeklyLog
        fields = [
            'id', 'status', 'week_no', 'logbook', 'logbook_entries',
            'comment', 'week_start_date', 'week_end_date'
        ]
        read_only_fields = ['week_no', 'logbook', 'logbook_entries']

    def get_logbook_entries(self, obj):
        return [
            {
                'id': entry.id,
                'description': entry.description,
                'created_at': entry.created_at,
                'is_immutable': entry.is_immutable,
                'status': 'approved' if entry.is_immutable else 'pending_approval',
                'feedback': entry.feedback
            }
            for entry in obj.logbook_entries.all()
        ]

    def create(self, validated_data):
        logbook = self.context['logbook']

        weekly_log = WeeklyLog(logbook=logbook, **validated_data)
        weekly_log.full_clean()  # Ensures clean() runs and sets week_no
        weekly_log.save()
        return weekly_log

    def update(self, instance, validated_data):
        # Disallow week number or logbook changes
        validated_data.pop('week_no', None)
        validated_data.pop('logbook', None)

        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Include detailed logbook entries information
        data['logbook_entries'] = self.get_logbook_entries(instance)
        return data
