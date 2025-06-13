from rest_framework import serializers
from apps.logbooks.models import Logbook


class LogbookSerializer(serializers.ModelSerializer):
    weekly_logs = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Logbook
        fields = ['id', 'status', 'internship', 'weekly_logs']