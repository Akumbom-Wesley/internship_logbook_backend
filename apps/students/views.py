from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from apps.students.models import Student
from apps.students.serializers import StudentSerializer
from apps.internships.models import InternshipRequest
from apps.internships.serializers import InternshipRequestSerializer, InternshipRequestCreateSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Student.objects.all()
        return Student.objects.filter(user=self.request.user)


class CreateInternshipRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'student':
            return Response({"error": "Only students can create internship requests."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            student = request.user.student
        except Student.DoesNotExist:
            return Response({"error": "Student profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InternshipRequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        internship_request = serializer.save(student=student)
        return Response(InternshipRequestSerializer(internship_request).data, status=status.HTTP_201_CREATED)


class StudentInternshipRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'student':
            return Response({"error": "Only students can view their internship requests."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            student = request.user.student
        except Student.DoesNotExist:
            return Response({"error": "Student profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        requests = InternshipRequest.objects.filter(student=student)
        serializer = InternshipRequestSerializer(requests, many=True)
        return Response(serializer.data)
