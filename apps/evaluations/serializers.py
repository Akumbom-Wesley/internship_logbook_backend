from django.db import transaction
from rest_framework import serializers
from apps.evaluations.models import Evaluation
from apps.evaluation_categories.models import EvaluationCategory
from apps.evaluation_category_subfields.models import EvaluationCategorySubfield


class EvaluationSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(write_only=True)

    class Meta:
        model = Evaluation
        fields = ['id', 'comments', 'total_score', 'categories']
        read_only_fields = ['total_score']

    def to_representation(self, instance):
        from apps.evaluation_categories.serializers import EvaluationCategorySerializer
        data = super().to_representation(instance)
        data['categories'] = EvaluationCategorySerializer(instance.categories.all(), many=True).data
        return data

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        internship = validated_data['internship']

        # Check if internship is completed
        if internship.status != 'completed':
            raise serializers.ValidationError("Internship must be completed before evaluation.")

        # Check if supervisor owns the internship
        request = self.context['request']
        if internship.supervisor.user != request.user:
            raise serializers.ValidationError("You are not authorized to evaluate this internship.")

        # Validate that we have exactly 5 categories
        if len(categories_data) != 5:
            raise serializers.ValidationError("An evaluation must have exactly 5 categories.")

        # Use transaction to ensure atomicity
        with transaction.atomic():
            # Create evaluation without triggering validation
            evaluation = Evaluation.objects.create(**validated_data)

            # Create categories and subfields
            for cat_data in categories_data:
                subfields_data = cat_data.get('subfields', [])
                template_id = cat_data.get('template_id')

                if template_id is None:
                    raise serializers.ValidationError("Category template_id is required.")

                # Validate that each category has exactly 4 subfields
                if len(subfields_data) != 4:
                    raise serializers.ValidationError("Each category must have exactly 4 subfields.")

                category = EvaluationCategory.objects.create(
                    evaluation=evaluation,
                    template_id=template_id
                )

                # Create all subfields for this category
                for sf_data in subfields_data:
                    template_id = sf_data.get('template_id')
                    score = sf_data.get('score')

                    if template_id is None:
                        raise serializers.ValidationError("Subfield template_id is required.")
                    if score is None:
                        raise serializers.ValidationError("Subfield score is required.")

                    EvaluationCategorySubfield.objects.create(
                        category=category,
                        template_id=template_id,
                        score=score
                    )

                # Now calculate the category score after all subfields are created
                category.calculate_score()
                category.save(update_fields=['subfields_total'])

            # Finally, run the full evaluation validation and score calculation
            evaluation.clean()
            evaluation.calculate_score()
            evaluation.save(update_fields=['total_score'])

        return evaluation