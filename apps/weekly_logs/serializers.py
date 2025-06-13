from rest_framework import serializers
from apps.weekly_logs.models import WeeklyLog
from apps.logbook_entries.models import LogbookEntry
from django.utils import timezone


class WeeklyLogSerializer(serializers.ModelSerializer):
    logbook_entries = serializers.SerializerMethodField()

    class Meta:
        model = WeeklyLog
        fields = ['id', 'status', 'week_no', 'logbook', 'logbook_entries', 'comment']
        read_only_fields = ['week_no', 'logbook_entries']

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
        # Get logbook_id from context
        logbook_id = self.context.get('logbook_id')
        if not logbook_id:
            raise serializers.ValidationError("Logbook ID is required.")

        validated_data['logbook_id'] = logbook_id
        validated_data.pop('week_no', None)  # Ensure week_no is not provided
        return super().create(validated_data)

    def validate(self, data):
        logbook_id = self.context.get('logbook_id')
        if not logbook_id:
            raise serializers.ValidationError({"logbook_id": "Logbook ID is required in context."})

        if not self.instance:
            raise serializers.ValidationError({"instance": "No weekly log instance provided."})

        if str(self.instance.logbook.id) != str(logbook_id):
            raise serializers.ValidationError({"logbook_id": "Logbook ID mismatch."})

        # If approving, ensure all log entries are immutable
        if data.get('status') == 'approved':
            if self.instance.logbook_entries.filter(is_immutable=False).exists():
                raise serializers.ValidationError(
                    {"status": "Cannot approve weekly log with unapproved entries."}
                )

        return data

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        if not instance.id:
            instance.save()  # Save to get PK before accessing relations
        data = super().to_representation(instance)
        data['logbook_entries'] = [str(entry) for entry in instance.logbook_entries.all()]
        return data