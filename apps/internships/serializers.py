from rest_framework import serializers

from apps.internships.models import InternshipRequest, Internship
from apps.supervisors.serializers import SupervisorSerializer
from ..academic_years.models import AcademicYear


class InternshipRequestSerializer(serializers.ModelSerializer):
    # Use string references for the related serializers to avoid circular imports
    student = serializers.StringRelatedField()
    company = serializers.StringRelatedField()

    class Meta:
        model = InternshipRequest
        fields = ['id', 'student', 'company', 'academic_year', 'start_date', 'end_date', 'job_description', 'status']
        read_only_fields = ['status']

    def get_student(self, obj):
        from apps.students.serializers import StudentSerializer
        return StudentSerializer(obj.student, context=self.context).data

    def get_company(self, obj):
        from apps.companies.serializers import CompanySerializer
        return CompanySerializer(obj.company, context=self.context).data

    def validate(self, data):
        # Ensure academic_year exists
        academic_year_id = data.get('academic_year').id
        if not AcademicYear.objects.filter(id=academic_year_id).exists():
            raise serializers.ValidationError("Invalid academic year.")
        return data


class InternshipRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipRequest
        fields = ['company', 'academic_year', 'start_date', 'end_date', 'job_description']

    def validate(self, data):
        # Ensure academic_year exists
        academic_year_id = data.get('academic_year').id
        if not AcademicYear.objects.filter(id=academic_year_id).exists():
            raise serializers.ValidationError("Invalid academic year.")
        return data


class InternshipSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    company = serializers.StringRelatedField()
    supervisor = SupervisorSerializer(read_only=True)

    class Meta:
        model = Internship
        fields = ['id', 'student', 'company', 'academic_year', 'start_date', 'end_date',
                  'job_description', 'supervisor', 'status']
