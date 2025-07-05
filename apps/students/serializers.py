from rest_framework import serializers

from apps.internships.serializers import InternshipRequestSerializer
from apps.students.models import Student
from apps.departments.serializers import DepartmentSerializer


class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    internship_requests = InternshipRequestSerializer(read_only=True, many=True)

    class Meta:
        model = Student
        fields = ['matricule_num', 'department', 'level', 'internship_requests']

    def get_internship_requests(self, obj):
        from apps.internships.serializers import InternshipRequestSerializer
        internship_requests = obj.internship_requests.all()
        return InternshipRequestSerializer(internship_requests, many=True, context=self.context).data