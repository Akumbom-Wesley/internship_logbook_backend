from django.db import models

from apps.companies.models import Company
from apps.core.models import BaseModel
from apps.users.models import User


class Supervisor(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.user.full_name
