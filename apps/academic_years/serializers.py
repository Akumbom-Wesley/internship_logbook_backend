from rest_framework.serializers import ModelSerializer
from .models import AcademicYear

class AcademicYearSerializer(ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'