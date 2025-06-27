from django.http import FileResponse
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.evaluations.models import Evaluation
from apps.evaluations.serializers import EvaluationSerializer
from apps.internships.models import Internship
from rest_framework.exceptions import ValidationError
from .utils import generate_evaluation_pdf
import os
from datetime import datetime
from django.conf import settings

class EvaluationCreateView(CreateAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        internship_id = self.kwargs.get('internship_id')
        try:
            internship = Internship.objects.get(id=internship_id)
        except Internship.DoesNotExist:
            raise ValidationError("Internship not found.")

        if Evaluation.objects.filter(internship=internship).exists():
            raise ValidationError("This internship already has an evaluation.")

        serializer.save(internship=internship)


class EvaluationPDFDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, internship_id):
        try:
            evaluation = Evaluation.objects.select_related(
                'internship__student__user',
                'internship__company',
                'internship__supervisor__user'
            ).prefetch_related(
                'categories__template',
                'categories__subfields__template'
            ).get(internship_id=internship_id)
        except Evaluation.DoesNotExist:
            return Response({"error": "Evaluation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Auth check: only admin, supervisor, or that student
        user = request.user
        internship = evaluation.internship
        if (user != internship.student.user and
                user != internship.supervisor.user and
                user.role not in ['super_admin', 'lecturer', 'company_admin']):
            return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

        try:
            pdf_buffer = generate_evaluation_pdf(evaluation)
            pdf_buffer.seek(0)  # Important: reset buffer position

            # Save PDF to media folder after successful generation
            self.save_pdf_to_media(pdf_buffer, internship_id, evaluation)

            # Reset buffer position for response
            pdf_buffer.seek(0)

            response = FileResponse(
                pdf_buffer,
                content_type='application/pdf',
                filename=f'internship_evaluation_report_{internship_id}.pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="internship_evaluation_report_{internship_id}.pdf"'
            return response

        except Exception as e:
            return Response(
                {"error": f"Error generating PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def save_pdf_to_media(self, pdf_buffer, internship_id, evaluation):
        """Save the PDF to media/evaluation_pdfs/ folder"""
        try:
            # Create the directory path
            folder_name = 'evaluation_pdfs'
            media_folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)

            # Ensure the directory exists
            os.makedirs(media_folder_path, exist_ok=True)

            # Create filename with timestamp for uniqueness
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            student_name = getattr(evaluation.internship.student.user, 'full_name', 'Unknown')
            # Clean the student name for filename (remove spaces and special characters)
            clean_student_name = ''.join(c for c in student_name if c.isalnum() or c in (' ', '-', '_')).replace(' ',
                                                                                                                 '_')
            filename = f'evaluation_{internship_id}_{clean_student_name}_{timestamp}.pdf'

            # Full file path
            file_path = os.path.join(media_folder_path, filename)

            # Save the file
            pdf_buffer.seek(0)  # Reset buffer position
            with open(file_path, 'wb') as f:
                f.write(pdf_buffer.read())

            print(f"PDF saved successfully at: {file_path}")

        except Exception as e:
            print(f"Error saving PDF to media folder: {str(e)}")
            # Don't raise the exception as we still want the download to work
            # even if saving fails