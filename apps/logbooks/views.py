from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.logbooks.models import Logbook
from apps.logbooks.serializers import LogbookSerializer


class LogbookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, internship_id=None):
        if not internship_id:
            return Response({"error": "Internship ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        logbooks = Logbook.objects.filter(internship_id=internship_id)
        serializer = LogbookSerializer(logbooks, many=True)
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