from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.internships.models import InternshipRequest, Internship
from apps.internships.serializers import InternshipSerializer, InternshipRequestSerializer
from apps.companies.models import CompanyAdmin
from apps.supervisors.models import Supervisor


class ApproveInternshipRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        # Check 1: Role must be company_admin
        if request.user.role != 'company_admin':
            return Response({"error": "Only company admins can approve internship requests."},
                            status=status.HTTP_403_FORBIDDEN)

        # Check 2: Company admin profile must exist
        try:
            company_admin = request.user.company_admin
        except CompanyAdmin.DoesNotExist:
            return Response({"error": "Company admin profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Check 3: Internship request must exist and belong to the company admin's company
        try:
            internship_request = InternshipRequest.objects.get(id=request_id, status='pending')
        except InternshipRequest.DoesNotExist:
            return Response({"error": "Internship request not found or already processed."},
                            status=status.HTTP_404_NOT_FOUND)

        if internship_request.company != company_admin.company:
            return Response({"error": "This request does not belong to your company."},
                            status=status.HTTP_403_FORBIDDEN)

        # Check 4: Supervisor ID must be provided
        supervisor_id = request.data.get('supervisor_id')
        if not supervisor_id:
            return Response({"error": "Supervisor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # # Check 5: Supervisor status must be approved
        if internship_request.company.supervisor_set.filter(id=supervisor_id, status='approved').exists() is False:
            return Response({"error": "Supervisor is not approved."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            supervisor = Supervisor.objects.get(id=supervisor_id)
        except Supervisor.DoesNotExist:
            return Response({"error": "Invalid supervisor ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Internship
        internship = Internship.objects.create(
            student=internship_request.student,
            company=internship_request.company,
            academic_year=internship_request.academic_year,
            start_date=internship_request.start_date,
            end_date=internship_request.end_date,
            job_description=internship_request.job_description,
            supervisor=supervisor,
            status='waiting'  # Default status, updated in save()
        )

        # Update request status
        internship_request.status = 'approved'
        internship_request.save()

        # Serialize the internship before returning
        serializer = InternshipSerializer(internship)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyAdminInternshipRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'company_admin':
            return Response({"error": "Only company admins can view internship requests."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            company_admin = request.user.company_admin
        except Supervisor.DoesNotExist:
            return Response({"error": "Company Admin profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        requests = InternshipRequest.objects.filter(company=company_admin.company, status='pending')
        serializer = InternshipRequestSerializer(requests, many=True)
        return Response(serializer.data)
