from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializers import UserSerializer, RoleSelectionSerializer
from apps.users.models import User
from apps.students.models import Student
from apps.supervisors.models import Supervisor
from apps.departments.models import Department
from apps.companies.models import Company
from apps.utils.emails import send_verification_email


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class CurrentUserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RoleSelectionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RoleSelectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        role = serializer.validated_data['role']

        if user.role != 'user':
            return Response({"error": "Role already selected."}, status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.save()

        if role == 'student':
            matricule_num = serializer.validated_data.get('matricule_num')
            department_id = serializer.validated_data.get('department_id')
            if not (matricule_num and department_id):
                return Response({"error": "matricule_num and department_id required for student role."},
                                status=status.HTTP_400_BAD_REQUEST)
            department = Department.objects.get(id=department_id)
            Student.objects.create(user=user, matricule_num=matricule_num, department=department)
        elif role == 'supervisor':
            company_id = serializer.validated_data.get('company_id')
            if not company_id:
                return Response({"error": "company_id required for supervisor role."},
                                status=status.HTTP_400_BAD_REQUEST)
            company = Company.objects.get(id=company_id)
            supervisor = Supervisor.objects.create(user=user, company=company, status='pending')
            send_verification_email(supervisor, request)

        return Response({"message": f"Role set to {role}."}, status=status.HTTP_200_OK)


class VerifySupervisorView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, supervisor_id):
        try:
            supervisor = Supervisor.objects.get(id=supervisor_id, status='pending')
            supervisor.status = 'approved'
            supervisor.save()
            return Response({"message": "Supervisor verified successfully."}, status=status.HTTP_200_OK)
        except Supervisor.DoesNotExist:
            return Response({"error": "Invalid or already verified supervisor."}, status=status.HTTP_400_BAD_REQUEST)