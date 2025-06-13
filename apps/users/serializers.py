from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from ..students.models import Student
from ..students.serializers import StudentSerializer
from ..supervisors.models import Supervisor
from ..supervisors.serializers import SupervisorSerializer
from ..companies.models import CompanyAdmin
from ..companies.serializers import CompanyAdminSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_id = serializers.CharField(source='id', read_only=True)
    student = serializers.SerializerMethodField()
    supervisor = serializers.SerializerMethodField()
    company_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'full_name', 'email', 'contact', 'role', 'image', 'password',
                  'student', 'supervisor', 'company_admin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.method == 'POST':
            self.fields['full_name'].required = True
            self.fields['contact'].required = True
            self.fields['email'].required = True
            self.fields['image'].required = False

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_student(self, obj):
        try:
            student = obj.student
            return StudentSerializer(student).data
        except Student.DoesNotExist:
            return None

    def get_supervisor(self, obj):
        try:
            supervisor = obj.supervisor
            return SupervisorSerializer(supervisor).data
        except Supervisor.DoesNotExist:
            return None

    def get_company_admin(self, obj):
        try:
            company_admin = obj.company_admin
            return CompanyAdminSerializer(company_admin).data
        except CompanyAdmin.DoesNotExist:
            return None


class RoleSelectionSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=['student', 'supervisor'])
    matricule_num = serializers.CharField(max_length=10, required=False)
    department_id = serializers.IntegerField(required=False)
    company_id = serializers.IntegerField(required=False)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.role == 'student':
            student = user.student
            try:
                # Decrypt using server-held key; no password needed
                decrypted_key = student.get_private_key()
            except Exception as e:
                raise serializers.ValidationError("Failed to decrypt private key.") from e
        return data
