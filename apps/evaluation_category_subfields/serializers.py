from rest_framework import serializers
from apps.evaluation_category_subfields.models import EvaluationCategorySubfield

class EvaluationCategorySubfieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCategorySubfield
        fields = ['id', 'name', 'score']