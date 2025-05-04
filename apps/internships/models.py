from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.academic_years.models import AcademicYear
from apps.companies.models import Company
from apps.core.models import BaseModel
from apps.lecturers.models import Lecturer
from apps.students.models import Student
from apps.supervisors.models import Supervisor


class Internship(BaseModel):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('ongoing', 'Ongoing'),
        ('completed', 'completed'),
        ('cancelled', 'Cancelled')
    ]

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    job_description = models.TextField(max_length=1000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='internships')

    def save(self, *args, **kwargs):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be later than start date.")

        if not self.pk or 'status' not in self.__dict__ or self.__dict__['status'] is None:  # Only on creation or status unset
            today = timezone.now().date()
            start_date = self.start_date.date()
            self.status = 'ongoing' if start_date <= today else 'waiting'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.company.name}"


class InternshipRequest(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='internship_requests')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='internship_requests')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    job_description = models.TextField(max_length=1000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = "Internship Request"
        verbose_name_plural = "Internship Requests"

    def __str__(self):
        return f"{self.student} - {self.company} ({self.status})"