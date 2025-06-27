from rest_framework.generics import ListAPIView
from .serializers import AcademicYearSerializer
from .models import AcademicYear
from rest_framework.permissions import IsAuthenticated

class ListAcademicYearView(ListAPIView):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAuthenticated]