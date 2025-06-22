from rest_framework import serializers

from apps.internships.models import InternshipRequest, Internship
from apps.supervisors.serializers import SupervisorSerializer
from ..academic_years.models import AcademicYear
from apps.companies.serializers import CompanySerializer
from apps.companies.models import CompanyAdmin


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
    student = serializers.SerializerMethodField()
    company = serializers.StringRelatedField()
    supervisor = SupervisorSerializer(read_only=True)

    class Meta:
        model = Internship
        fields = ['id', 'student', 'company', 'academic_year', 'start_date', 'end_date',
                  'job_description', 'supervisor', 'status']

    def get_student(self, obj):
        from apps.students.serializers import StudentSerializer
        return StudentSerializer(obj.student).data

    def get_company(self, obj):
        return CompanySerializer(obj.company, context=self.context).data

class InternshipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ['start_date', 'end_date', 'job_description', 'status', 'supervisor', 'lecturer']
        # No read_only_fields; all fields are editable by company admins


class InternshipBulkUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Internship.STATUS_CHOICES, required=True)

    def validate_company_id(self, value):
        request = self.context.get('request')
        if request and request.user.role == 'company_admin':
            company_admin = request.user.company_admin
            if str(company_admin.company.id) != str(value):
                raise serializers.ValidationError("You can only update internships for your company.")
        return value