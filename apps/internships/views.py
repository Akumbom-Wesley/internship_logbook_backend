from apps.internships.serializers import InternshipSerializer, InternshipUpdateSerializer, InternshipRequestSerializer, InternshipBulkUpdateSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from apps.internships.models import Internship
from ..utils.internship_report import InternshipReportGenerateView

class InternshipListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):
        if request.user.role not in ['company_admin', 'super_admin']:
            return Response(
                {"error": "Only company admins and super admins can list internships."},
                status=status.HTTP_403_FORBIDDEN
            )

        internships = Internship.objects.filter(company=company_id)

        # Filtering
        status_filter = request.query_params.get('status')
        year_filter = request.query_params.get('academic_year')

        if status_filter:
            internships = internships.filter(status=status_filter)
        if year_filter:
            internships = internships.filter(academic_year=year_filter)

        serializer = InternshipSerializer(internships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#TODO: Add view to list internship by student and company id

class InternshipDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, internship_id):
        if request.user.role not in ['company_admin', 'super_admin']:
            return Response({"error": "Only company admins and super admins can view internship details."},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            internship = Internship.objects.get(id=internship_id)
        except Internship.DoesNotExist:
            return Response({"error": "Internship not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InternshipSerializer(internship)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InternshipMyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'student':
            return Response({"error": "Only students can view their internships."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            student = request.user.student
        except AttributeError:
            return Response({"error": "Student profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        internships = Internship.objects.filter(student=student)
        serializer = InternshipSerializer(internships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InternshipUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, internship_id):
        if request.user.role != 'company_admin':
            return Response({"error": "Only company admins can update internships."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            company_admin = request.user.company_admin
        except AttributeError:
            return Response({"error": "Company admin profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            internship = Internship.objects.get(id=internship_id)
        except Internship.DoesNotExist:
            return Response({"error": "Internship not found."}, status=status.HTTP_404_NOT_FOUND)

        if internship.company != company_admin.company:
            return Response({"error": "This internship does not belong to your company."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = InternshipUpdateSerializer(internship, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class OngoingInternshipView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != 'student':
            return Response({"error": "Only students can access their ongoing internship."}, status=status.HTTP_403_FORBIDDEN)

        try:
            internship = Internship.objects.get(student__user=user, status='ongoing')
        except Internship.DoesNotExist:
            return Response({"error": "No ongoing internship found for this student."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InternshipSerializer(internship)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InternshipDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, internship_id):
        if request.user.role not in ['company_admin', 'super_admin']:
            return Response({"error": "Only company admins and super admins can delete internships."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            if request.user.role == 'company_admin':
                company_admin = request.user.company_admin
        except AttributeError:
            return Response({"error": "Company admin profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            internship = Internship.objects.get(id=internship_id)
        except Internship.DoesNotExist:
            return Response({"error": "Internship not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'company_admin' and internship.company != company_admin.company:
            return Response({"error": "This internship does not belong to your company."},
                            status=status.HTTP_403_FORBIDDEN)

        internship.delete()
        return Response({"message": "Internship deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class InternshipBulkUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, company_id):
        if request.user.role != 'company_admin':
            return Response({"error": "Only company admins can perform bulk updates."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            company_admin = request.user.company_admin
        except AttributeError:
            return Response({"error": "Company admin profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InternshipBulkUpdateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']

        if str(company_admin.company.id) != str(company_id):
            return Response({"error": "You can only update internships for your company."},
                            status=status.HTTP_403_FORBIDDEN)

        # Fetch all internships for the specified company
        internships = Internship.objects.filter(company_id=company_id)
        if not internships.exists():
            return Response({"error": "No internships found for this company."},
                            status=status.HTTP_404_NOT_FOUND)

        # Update status for all internships under the company
        updated_count = internships.update(status=new_status)
        return Response({"message": f"Updated status to '{new_status}' for {updated_count} internships."},
                        status=status.HTTP_200_OK)


class InternshipReportDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, internship_id):
        try:
            internship = Internship.objects.select_related(
                'student__user', 'student__department__school',
                'company', 'supervisor__user',
                'logbook'
            ).prefetch_related(
                'logbook__weekly_logs__logbook_entries'
            ).get(id=internship_id, student__user=request.user)
        except Internship.DoesNotExist:
            return Response({"error": "Internship not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        if internship.status != 'completed':
            return Response({"error": "Internship must be completed before report generation."},
                            status=status.HTTP_400_BAD_REQUEST)

        buffer = generate_internship_report(internship)
        filename = f"internship_report_{request.user.full_name.replace(' ', '_')}.docx"
        return FileResponse(buffer, as_attachment=True, filename=filename)

