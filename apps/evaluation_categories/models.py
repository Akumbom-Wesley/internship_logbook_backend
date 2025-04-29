from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.evaluations.models import Evaluation


class EvaluationCategory(BaseModel):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)
    subfields_total = models.IntegerField(default=0, editable=False)

    def clean(self):
        # Check subfield limit
        subfield_count = self.subfields.count()
        if subfield_count > 4:
            raise ValidationError("An evaluation category cannot have more than 4 subfields.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        # Compute subfields_total
        self.subfields_total = sum(subfield.score for subfield in self.subfields.all())
        self.save(update_fields=['subfields_total'])

    class Meta:
        verbose_name = "Evaluation Category"
        verbose_name_plural = "Evaluation Categories"

    def __str__(self):
        return self.name