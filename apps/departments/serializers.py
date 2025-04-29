from rest_framework import serializers

from apps.departments.models import Department
from apps.schools.serializers import SchoolSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'school']
