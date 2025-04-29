from rest_framework import serializers
from apps.students.models import Student
from apps.departments.serializers import DepartmentSerializer


class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['matricule_num', 'departments']