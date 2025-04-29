from django.core.exceptions import ValidationError
from django.db import models

from apps.academic_years.models import AcademicYear
from apps.companies.models import Company
from apps.core.models import BaseModel
from apps.lecturers.models import Lecturer
from apps.students.models import Student
from apps.supervisors.models import Supervisor


class Internship(BaseModel):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'completed'),
        ('cancelled', 'Cancelled')
    ]

    start_date = models.DateTimeField()
    end_date = models.DateTimeField
    job_description = models.TextField(max_length=1000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def save(self, *args, **kwargs):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be later than start date.")
        super().save(*args, **kwargs)

    def __str__(self):
        student_names = ', '.join(student.user.full_name for student in self.students.all())
        return f"{student_names} - {self.company.name}"