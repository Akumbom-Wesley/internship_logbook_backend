from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.internships.models import Internship
from apps.internships.serializers import InternshipSerializer
from apps.supervisors.models import Supervisor
from apps.students.models import Student
from apps.students.serializers import StudentSerializer
from apps.logbook_entries.models import LogbookEntry

class SupervisorAssignedInternshipsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check 1: Role must be supervisor
        if request.user.role != 'supervisor':
            return Response({"error": "Only supervisors can view assigned internships."},
                            status=status.HTTP_403_FORBIDDEN)

        # Check 2: Supervisor profile must exist and be approved
        try:
            supervisor = request.user.supervisor
        except Supervisor.DoesNotExist:
            return Response({"error": "Supervisor profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        if supervisor.status != 'approved':
            return Response({"error": "Only approved supervisors can view assigned internships."},
                            status=status.HTTP_403_FORBIDDEN)

        # Get internships assigned to the supervisor
        students = Internship.student.objects.filter(supervisor=supervisor)
        serializer = InternshipSerializer(internships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupervisorAssignedStudentsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class =  StudentSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role != 'supervisor':
            return User.objects.none()  # Or raise permission denied

        # Get the supervisor object
        try:
            supervisor = user.supervisor
        except AttributeError:
            return User.objects.none()

        # Get student users assigned to this supervisor via internship
        students = Student.objects.filter(
            internships__supervisor=supervisor
        ).distinct()

        return students

class SupervisorStudentLogActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != 'supervisor':
            return Response({"error": "Only supervisors can view this activity."}, status=status.HTTP_403_FORBIDDEN)

        try:
            supervisor = user.supervisor
        except AttributeError:
            return Response({"error": "Supervisor profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Get all log entries for internships supervised by this supervisor
        log_entries = LogbookEntry.objects.filter(
            weekly_log__logbook__internship__supervisor=supervisor
        ).select_related(
            'weekly_log',
            'weekly_log__logbook',
            'weekly_log__logbook__internship',
            'weekly_log__logbook__internship__student',
            'weekly_log__logbook__internship__student__user',
        ).order_by('-created_at')[:5]  # Get latest 3 entries

        data = []
        for entry in log_entries:
            student = entry.weekly_log.logbook.internship.student
            data.append({
                "student": {
                    "id": student.id,
                    "name": student.user.full_name,
                    "matricule_num": student.matricule_num,
                    "department": str(student.department)
                },
                "entry_id": entry.id,
                "week_no": entry.weekly_log.week_no,
                "entry_date": entry.created_at.strftime('%Y-%m-%d %H:%M'),
                "description": entry.description[:100],  # preview
                "is_immutable": entry.is_immutable
            })

        return Response(data, status=status.HTTP_200_OK)