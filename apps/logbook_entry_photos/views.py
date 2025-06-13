from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.logbook_entry_photos.models import LogbookEntryPhoto
from apps.logbook_entry_photos.serializers import LogbookEntryPhotoSerializer


class LogbookEntryPhotoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        photos = LogbookEntryPhoto.objects.all()
        serializer = LogbookEntryPhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogbookEntryPhotoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, photo_id):
        try:
            photo = LogbookEntryPhoto.objects.get(id=photo_id)
        except LogbookEntryPhoto.DoesNotExist:
            return Response({"error": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LogbookEntryPhotoSerializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogbookEntryPhotoCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'student':
            return Response({"error": "Only students can upload logbook entry photos."}, status=status.HTTP_403_FORBIDDEN)
        serializer = LogbookEntryPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogbookEntryPhotoUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, photo_id):
        if request.user.role != 'student':
            return Response({"error": "Only students can update logbook entry photos."}, status=status.HTTP_403_FORBIDDEN)
        try:
            photo = LogbookEntryPhoto.objects.get(id=photo_id)
        except LogbookEntryPhoto.DoesNotExist:
            return Response({"error": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
        if photo.log_entry.weekly_log.logbook.internship.student.user != request.user:
            return Response({"error": "You can only update photos for your own logbook entries."}, status=status.HTTP_403_FORBIDDEN)
        serializer = LogbookEntryPhotoSerializer(photo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogbookEntryPhotoDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, photo_id):
        if request.user.role != 'student':
            return Response({"error": "Only students can delete logbook entry photos."}, status=status.HTTP_403_FORBIDDEN)
        try:
            photo = LogbookEntryPhoto.objects.get(id=photo_id)
        except LogbookEntryPhoto.DoesNotExist:
            return Response({"error": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
        if photo.log_entry.weekly_log.logbook.internship.student.user != request.user:
            return Response({"error": "You can only delete photos for your own logbook entries."}, status=status.HTTP_403_FORBIDDEN)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)