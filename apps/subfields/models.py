from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.evaluation_categories.models import EvaluationCategory


class Subfield(BaseModel):
    category = models.ForeignKey(EvaluationCategory, on_delete=models.CASCADE, related_name='subfields')
    name = models.CharField(max_length=50)
    score = models.IntegerField()

    def clean(self):
        if not (0 <= self.score <= 5):
            raise ValidationError("Score must be between 0 and 5.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        # Update the category's subfields_total
        self.category.save()

    def __str__(self):
        return f"{self.name} - {self.category.name}"