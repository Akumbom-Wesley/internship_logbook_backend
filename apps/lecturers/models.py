from django.db import models

from apps.core.models import BaseModel
from apps.departments.models import Department
from apps.users.models import User


class Lecturer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')

    def __str__(self):
        return self.user.full_name