from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from apps.core.models import BaseModel
from apps.internships.models import Internship


class Logbook(BaseModel):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending_approval', 'Pending Approval')
    ]

    status = models.CharField(choices=STATUS_CHOICES, default='pending_approval')
    internship = models.OneToOneField(Internship, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['internship'], name='unique_logbook_per_internship')
        ]

    def __str__(self):
        return f"{self.internship.student.user.full_name} - {self.status}"

    def clean(self):
        if self.internship.end_date < timezone.now().date() and self.status != 'approved':
            raise ValidationError("Logbook cannot be created or updated after internship end date unless approved.")