from rest_framework import serializers
from apps.supervisors.models import Supervisor
from apps.companies.serializers import CompanySerializer


class SupervisorSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Supervisor
        fields = ['company', 'status']