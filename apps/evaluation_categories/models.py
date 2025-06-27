from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel
from apps.evaluations.models import Evaluation, EvaluationTemplate


class EvaluationCategory(BaseModel):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='categories')
    template = models.ForeignKey(EvaluationTemplate, on_delete=models.CASCADE)
    subfields_total = models.IntegerField(default=0, editable=False)

    @property
    def name(self):
        return self.template.name

    def clean(self):
        # Only validate if the category has been saved and subfields exist
        if self.pk and self.subfields.count() != 4:
            raise ValidationError("Each category must contain exactly 4 subfields.")

    def calculate_score(self):
        self.subfields_total = sum(sf.score for sf in self.subfields.all())

    def save(self, *args, **kwargs):
        # First save without validation
        super().save(*args, **kwargs)

        # Only run validation and score calculation if subfields exist
        if self.subfields.exists():
            self.clean()
            self.calculate_score()
            super().save(update_fields=['subfields_total'])