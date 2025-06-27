from rest_framework import serializers
from apps.evaluation_categories.models import EvaluationCategory
from apps.evaluation_category_subfields.serializers import EvaluationCategorySubfieldSerializer

class EvaluationCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    subfields = EvaluationCategorySubfieldSerializer(many=True)
    template_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = EvaluationCategory
        fields = ['id', 'name', 'subfields_total', 'subfields', 'template_id']
        read_only_fields = ['subfields_total']
