from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel
from apps.internships.models import Internship


class Evaluation(BaseModel):
    total_score = models.IntegerField(default=0, editable=False)
    comments = models.TextField(max_length=1000, blank=True)
    internship = models.OneToOneField(Internship, on_delete=models.CASCADE, related_name='evaluation')

    def clean(self):
        # Only validate if the evaluation has been saved and categories exist
        if self.pk and self.categories.count() != 5:
            raise ValidationError("An evaluation must have exactly 5 categories.")

    def calculate_score(self):
        self.total_score = sum(cat.subfields_total for cat in self.categories.all())
        if self.total_score > 100:
            raise ValidationError("Total score cannot exceed 100.")

    def save(self, *args, **kwargs):
        # First save without validation
        super().save(*args, **kwargs)

        # Only run validation and score calculation if categories exist
        if self.categories.exists():
            self.clean()
            self.calculate_score()
            super().save(update_fields=['total_score'])


class EvaluationTemplate(BaseModel):
    """Template for hardcoded evaluation categories and subfields"""
    name = models.CharField(max_length=100, unique=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']