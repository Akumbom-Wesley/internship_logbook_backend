from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.logbooks.models import Logbook
from apps.logbooks.serializers import LogbookSerializer
from apps.internships.models import Internship

import os
from django.conf import settings
from rest_framework.views import APIView
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime
from apps.logbooks.utils import generate_logbook_pdf


class LogbookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, internship_id):
        try:
            logbook = Logbook.objects.get(internship__id=internship_id)
        except Logbook.DoesNotExist:
            return Response({"error": "Logbook not found for this internship."},
                            status=status.HTTP_404_NOT_FOUND)

        user = request.user
        internship = logbook.internship

        # Check if user is authorized to view this logbook
        if user.role == 'student' and internship.student.user != user:
            return Response({"error": "You can only view your own internship logbook."},
                            status=status.HTTP_403_FORBIDDEN)
        if user.role == 'supervisor' and internship.supervisor.user != user:
            return Response({"error": "You can only view logbooks for your supervised internships."},
                            status=status.HTTP_403_FORBIDDEN)
        if user.role not in ['student', 'supervisor', 'super_admin']:
            return Response({"error": "Unauthorized access to logbook."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = LogbookSerializer(logbook)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogbookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, logbook_id):
        try:
            logbook = Logbook.objects.get(id=logbook_id)
        except Logbook.DoesNotExist:
            return Response({"error": "Logbook not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LogbookSerializer(logbook)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogbookCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'student':
            return Response({"error": "Only students can create logbooks."}, status=status.HTTP_403_FORBIDDEN)
        serializer = LogbookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogbookUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, logbook_id):
        if request.user.role != 'supervisor':
            return Response({"error": "Only supervisors can update logbooks."}, status=status.HTTP_403_FORBIDDEN)
        try:
            logbook = Logbook.objects.get(id=logbook_id)
        except Logbook.DoesNotExist:
            return Response({"error": "Logbook not found."}, status=status.HTTP_404_NOT_FOUND)
        if logbook.internship.supervisor.user != request.user:
            return Response({"error": "You can only update logbooks for your internships."}, status=status.HTTP_403_FORBIDDEN)
        mutable_data = {k: v for k, v in request.data.items() if k == 'status'}
        if not mutable_data:
            return Response({"error": "Only status can be updated."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LogbookSerializer(logbook, data=mutable_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class OngoingLogbookByInternshipView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, internship_id):
        user = request.user

        if user.role != 'student':
            return Response({"error": "Only students can access their logbooks."}, status=status.HTTP_403_FORBIDDEN)

        try:
            internship = Internship.objects.get(id=internship_id, student__user=user)
        except Internship.DoesNotExist:
            return Response({"error": "Internship not found or does not belong to you."}, status=status.HTTP_404_NOT_FOUND)

        try:
            logbook = Logbook.objects.get(internship=internship, status='pending_approval')
        except Logbook.DoesNotExist:
            return Response({"error": "No ongoing (pending approval) logbook found for this internship."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = LogbookSerializer(logbook)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogbookDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, logbook_id):
        if request.user.role != 'student':
            return Response({"error": "Only students can delete logbooks."}, status=status.HTTP_403_FORBIDDEN)
        try:
            logbook = Logbook.objects.get(id=logbook_id)
        except Logbook.DoesNotExist:
            return Response({"error": "Logbook not found."}, status=status.HTTP_404_NOT_FOUND)
        if logbook.internship.student.user != request.user:
            return Response({"error": "You can only delete your own logbook."}, status=status.HTTP_403_FORBIDDEN)
        logbook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LogbookPDFDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'student':
            return Response({"error": "Only students can download their logbooks."}, status=status.HTTP_403_FORBIDDEN)

        try:
            internship = Internship.objects.get(student__user=user, status='completed')
        except Internship.DoesNotExist:
            return Response({"error": "Completed internship not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            logbook = Logbook.objects.prefetch_related('weekly_logs__logbook_entries').get(internship=internship)
        except Logbook.DoesNotExist:
            return Response({"error": "Logbook not found."}, status=status.HTTP_404_NOT_FOUND)

        # Generate PDF
        pdf_buffer = generate_logbook_pdf(logbook)

        # Ensure media/logbooks directory exists
        logbook_dir = os.path.join(settings.MEDIA_ROOT, 'logbooks')
        os.makedirs(logbook_dir, exist_ok=True)

        # Define file path
        filename = f"logbook_{internship.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        file_path = os.path.join(logbook_dir, filename)

        # Save PDF to file
        with open(file_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())

        # Serve the file
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)