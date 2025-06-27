from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.weekly_logs.models import WeeklyLog
from apps.logbooks.models import Logbook
from apps.weekly_logs.serializers import WeeklyLogSerializer


class WeeklyLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, logbook_id=None):
        if not logbook_id:
            return Response({"error": "Logbook ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        weekly_logs = WeeklyLog.objects.filter(logbook_id=logbook_id)
        serializer = WeeklyLogSerializer(weekly_logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeeklyLogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, weekly_log_id):
        try:
            weekly_log = WeeklyLog.objects.get(id=weekly_log_id)
        except WeeklyLog.DoesNotExist:
            return Response({"error": "Weekly log not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = WeeklyLogSerializer(weekly_log)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeeklyLogCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, logbook_id):
        try:
            logbook = Logbook.objects.get(id=logbook_id)
        except Logbook.DoesNotExist:
            return Response(
                {"error": "Logbook not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Authorization
        if not (request.user.role == 'student' and
                logbook.internship.student.user == request.user):
            return Response(
                {"error": "You are not authorized to create weekly logs."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = WeeklyLogSerializer(
            data=request.data,
            context={'logbook': logbook}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeeklyLogUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, logbook_id, weekly_log_id):
        try:
            weekly_log = WeeklyLog.objects.get(id=weekly_log_id)
        except WeeklyLog.DoesNotExist:
            return Response({"error": "Weekly log not found."}, status=status.HTTP_404_NOT_FOUND)

        # Verify the weekly log belongs to the specified logbook
        if weekly_log.logbook_id != logbook_id:
            return Response(
                {"error": "Weekly log does not belong to the specified logbook."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.role == 'supervisor':
            if weekly_log.logbook.internship.supervisor.user != request.user:
                return Response(
                    {"error": "You can only update weekly logs for your internships."},
                    status=status.HTTP_403_FORBIDDEN
                )

            mutable_data = {k: v for k, v in request.data.items() if k in ['status', 'comment']}
            if not mutable_data:
                return Response(
                    {"error": "No updatable fields (status or comment) provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = WeeklyLogSerializer(
                weekly_log,
                data=mutable_data,
                partial=True,
                context={
                    'logbook_id': logbook_id,
                    'request': request  # Pass request to serializer if needed
                }
            )

            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except (ValidationError, DRFValidationError) as e:
                error_detail = e.detail if hasattr(e, 'detail') else str(e)
                return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "Only supervisors can update weekly logs."},
                status=status.HTTP_403_FORBIDDEN
            )

class WeeklyLogDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, weekly_log_id):
        if request.user.role != 'student':
            return Response({"error": "Only students can delete weekly logs."}, status=status.HTTP_403_FORBIDDEN)
        try:
            weekly_log = WeeklyLog.objects.get(id=weekly_log_id)
        except WeeklyLog.DoesNotExist:
            return Response({"error": "Weekly log not found."}, status=status.HTTP_404_NOT_FOUND)
        if weekly_log.logbook.internship.student.user != request.user:
            return Response({"error": "You can only delete your own weekly logs."}, status=status.HTTP_403_FORBIDDEN)
        weekly_log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)