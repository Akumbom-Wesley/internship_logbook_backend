from django.db import models

from apps.core.models import BaseModel
from apps.internships.models import Internship


class Logbook(BaseModel):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(choices=STATUS_CHOICES, default='rejected')
    internship = models.OneToOneField(Internship, on_delete=models.CASCADE)

    def __str__(self):
        return self.status
