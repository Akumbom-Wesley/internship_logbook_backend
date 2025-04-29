from django.core.validators import EmailValidator
from django.db import models
from apps.core.models import BaseModel
from apps.users.models import validate_contact


class Company(BaseModel):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    contact = models.CharField(max_length=15, validators=[validate_contact])
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    email = models.CharField(max_length=50, unique=True, validators=[EmailValidator()])
    division = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name
