from django.core.exceptions import ValidationError
from django.db import models
from apps.core.models import BaseModel
from apps.internships.models import Internship


class Evaluation(BaseModel):
    total_score = models.IntegerField(default=0, editable=False)
    comments = models.TextField(max_length=1000, blank=True)
    internship = models.OneToOneField(Internship, on_delete=models.CASCADE, related_name='evaluation')

    def clean(self):
        category_count = self.categories.count()
        if category_count != 5:
            raise ValidationError("An evaluation must have exactly 5 categories.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clean()
        # Compute total_score as the sum of subfields_total from all categories
        self.total_score = sum(category.subfields_total for category in self.categories.all())
        if self.total_score > 100:
            raise ValidationError("Total score cannot exceed 100.")
        self.save(update_fields=['total_score'])

    def __str__(self):
        return f"Evaluation for {self.internship} - Score: {self.total_score}"