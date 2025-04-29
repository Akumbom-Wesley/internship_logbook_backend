from django.db import models

from apps.core.models import BaseModel
from apps.school.models import School


class Department(BaseModel):
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.school}"
