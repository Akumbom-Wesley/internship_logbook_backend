from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from apps.core.models import BaseModel
from apps.logbooks.models import Logbook


class WeeklyLog(BaseModel):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='rejected')
    week_no = models.PositiveIntegerField()
    logbook = models.ForeignKey(Logbook, on_delete=models.CASCADE, related_name='weekly_logs')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['week_no', 'logbook'], name='unique_week_no_per_logbook')
        ]

    def clean(self):
        log_entry_count = self.logbook.logbook_entries.filter(weekly_log=self).count()
        if log_entry_count >= 5:
            raise ValidationError("Cannot add more than 5 log entries per week (Mon-Fri).")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Week {self.week_no} - {self.logbook}"