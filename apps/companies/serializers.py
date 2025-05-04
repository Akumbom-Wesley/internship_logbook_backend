from rest_framework import serializers
from apps.companies.models import Company, CompanyAdmin


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'email']


class CompanyAdminSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = CompanyAdmin
        fields = ['id', 'company']
