from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.logbook_entries.models import LogbookEntry
from apps.logbook_entries.serializers import LogbookEntrySerializer


class LogbookEntryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, entry_id):
        try:
            entry = LogbookEntry.objects.get(id=entry_id)
        except LogbookEntry.DoesNotExist:
            return Response({"error": "Logbook entry not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LogbookEntrySerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogbookEntryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, weekly_log_id):
        try:
            logbook_entries = LogbookEntry.objects.filter(weekly_log_id=weekly_log_id)
        except LogbookEntry.DoesNotExist:
            return Response({"error": "No logbook entries found for this weekly log."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LogbookEntrySerializer(logbook_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogbookEntryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'student':
            return Response({"error": "Only students can create logbook entries."}, status=status.HTTP_403_FORBIDDEN)
        serializer = LogbookEntrySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogbookEntryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, entry_id):
        if request.user.role not in ['student', 'supervisor']:
            return Response({"error": "Only students or supervisors can update logbook entries."}, status=status.HTTP_403_FORBIDDEN)
        try:
            entry = LogbookEntry.objects.get(id=entry_id)
        except LogbookEntry.DoesNotExist:
            return Response({"error": "Logbook entry not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role == 'student' and entry.weekly_log.logbook.internship.student.user != request.user:
            return Response({"error": "You can only update your own logbook entries."}, status=status.HTTP_403_FORBIDDEN)
        if request.user.role == 'supervisor' and entry.weekly_log.logbook.internship.supervisor.user != request.user:
            return Response({"error": "You can only update entries for your internships."}, status=status.HTTP_403_FORBIDDEN)
        serializer = LogbookEntrySerializer(entry, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogbookEntryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, entry_id):
        if request.user.role != 'student':
            return Response({"error": "Only students can delete logbook entries."}, status=status.HTTP_403_FORBIDDEN)
        try:
            entry = LogbookEntry.objects.get(id=entry_id)
        except LogbookEntry.DoesNotExist:
            return Response({"error": "Logbook entry not found."}, status=status.HTTP_404_NOT_FOUND)
        if entry.weekly_log.logbook.internship.student.user != request.user:
            return Response({"error": "You can only delete your own logbook entries."}, status=status.HTTP_403_FORBIDDEN)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogbookEntryApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, entry_id):
        if request.user.role != 'supervisor':
            return Response({"error": "Only supervisors can approve logbook entries."}, status=status.HTTP_403_FORBIDDEN)
        try:
            entry = LogbookEntry.objects.get(id=entry_id)
        except LogbookEntry.DoesNotExist:
            return Response({"error": "Logbook entry not found."}, status=status.HTTP_404_NOT_FOUND)
        if entry.weekly_log.logbook.internship.supervisor.user != request.user:
            return Response({"error": "You can only approve entries for your internships."}, status=status.HTTP_403_FORBIDDEN)
        if not entry.signature or not entry.verify_signature(entry.signature):
            return Response({"error": "Invalid or missing signature."}, status=status.HTTP_400_BAD_REQUEST)
        entry.is_immutable = True
        entry.save()
        serializer = LogbookEntrySerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)