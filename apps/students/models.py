from django.db import models

from apps.core.models import BaseModel
from apps.department.models import Department
from apps.users.models import User, validate_matricule_num


class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    matricule_num = models.CharField(max_length=10, validators=[validate_matricule_num])

    def __str__(self):
        return f"{self.user.full_name} - {self.matricule_num}"

