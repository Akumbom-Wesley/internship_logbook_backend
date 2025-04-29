from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel


class AcademicYear(BaseModel):
    start_year = models.IntegerField(help_text="Start year of the academic period")
    end_year = models.IntegerField(help_text="End year of the academic period")
    label = models.CharField(
        max_length=9,
        editable=False,
        blank=True,
        help_text="Automatically generated as 'start_year/end_year'"
    )

    def save(self, *args, **kwargs):
        if self.end_year <= self.start_year:
            raise ValidationError("End year must be greater than start year.")
        self.label = f"{self.start_year}/{self.end_year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label
