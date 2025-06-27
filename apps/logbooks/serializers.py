from rest_framework import serializers
from apps.logbooks.models import Logbook
from apps.weekly_logs.serializers import WeeklyLogSerializer


class LogbookSerializer(serializers.ModelSerializer):
    weekly_logs = WeeklyLogSerializer(read_only=True, many=True)

    class Meta:
        model = Logbook
        fields = ['id', 'status', 'internship', 'weekly_logs']