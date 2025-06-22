from rest_framework import serializers
from apps.supervisors.models import Supervisor
from apps.companies.serializers import CompanySerializer


class SupervisorSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Supervisor
        fields = ['user_id', 'user_name', 'company', 'status']
