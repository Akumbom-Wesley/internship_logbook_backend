from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from apps.core.models import BaseModel
from apps.logbooks.models import Logbook


class WeeklyLog(BaseModel):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending_approval', 'Pending Approval')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_approval')
    week_no = models.PositiveIntegerField(editable=False)
    logbook = models.ForeignKey(Logbook, on_delete=models.CASCADE, related_name='weekly_logs')
    comment = models.TextField(max_length=500, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['week_no', 'logbook'], name='unique_week_no_per_logbook')
        ]

    def clean(self):
        internship = self.logbook.internship
        start_date = internship.start_date.date()
        end_date = internship.end_date.date()
        current_date = timezone.now().date()

        # Ensure current date is within internship range
        if current_date < start_date or current_date > end_date:
            raise ValidationError({
                "detail": "Weekly log can only be created within the internship period."
            })

        # Set week number (only during creation)
        if not self.pk:
            days_since_start = (current_date - start_date).days
            self.week_no = (days_since_start // 7) + 1

        # Prevent approval if not all entries are immutable
        if self.status == 'approved' and self.logbook_entries.filter(is_immutable=False).exists():
            raise ValidationError({
                "detail": "Cannot approve the weekly log until all log entries are approved."
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures clean() is always called
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Week {self.week_no} - {self.logbook}"