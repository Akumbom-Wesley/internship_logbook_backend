from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from ..students.models import Student
from ..students.serializers import StudentSerializer
from ..supervisors.models import Supervisor
from ..supervisors.serializers import SupervisorSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_id = serializers.CharField(source='id', read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'full_name', 'email', 'contact', 'role', 'image', 'password']
        read_only_fields = ['role']

    #TODO: Show student/supervisor info in response

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.method == 'POST':
            self.fields['full_name'].required = True
            self.fields['contact'].required = True
            self.fields['email'].required = True
            self.fields['image'].required = False
            self.fields.pop('role', None)
            self.fields.pop('student', None)
            self.fields.pop('supervisor', None)

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




class RoleSelectionSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=['student', 'supervisor'])
    matricule_num = serializers.CharField(max_length=10, required=False)
    department_id = serializers.IntegerField(required=False)
    company_id = serializers.IntegerField(required=False)
