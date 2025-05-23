from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.internships.models import Internship
from apps.internships.serializers import InternshipSerializer
from apps.supervisors.models import Supervisor


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
        internships = Internship.objects.filter(supervisor=supervisor)
        serializer = InternshipSerializer(internships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)