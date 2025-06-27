from django.db import models
from apps.core.models import BaseModel
from apps.evaluation_categories.models import EvaluationCategory
from apps.evaluations.models import EvaluationTemplate

class EvaluationSubfieldTemplate(BaseModel):
    """Template for hardcoded subfields"""
    category = models.ForeignKey(EvaluationTemplate, on_delete=models.CASCADE, related_name='subfield_templates')
    name = models.CharField(max_length=200)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']


class EvaluationCategorySubfield(BaseModel):
    category = models.ForeignKey(EvaluationCategory, on_delete=models.CASCADE, related_name='subfields')
    template = models.ForeignKey(EvaluationSubfieldTemplate, on_delete=models.CASCADE, related_name='subfields')
    score = models.IntegerField()

    @property
    def name(self):
        return self.template.name

    def clean(self):
        if not (0 <= self.score <= 5):
            raise ValidationError("Score must be between 0 and 5.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        # Only trigger category recalculation if this is not the initial creation
        # and if the category has all its subfields
        if self.pk and self.category.subfields.count() >= 4:
            self.category.calculate_score()
            self.category.save(update_fields=['subfields_total'])
