from django.db import models

from apps.core.models import BaseModel
from apps.weekly_logs.models import WeeklyLog


class LogbookEntryManager(models.Manager):
    def immutable(self):
        return self.filter(is_immutable=True)


class LogbookEntry(BaseModel):
    description = models.TextField(max_length=1000)
    is_immutable = models.BooleanField(default=False)
    feedback = models.TextField(max_length=500, blank=True)
    version = models.PositiveIntegerField(default=1)
    signature = models.TextField(blank=True)  # Store the digital signature

    weekly_log = models.ForeignKey(WeeklyLog, on_delete=models.CASCADE, related_name='logbook_entries')

    objects = LogbookEntryManager()

    class Meta:
        verbose_name = "Logbook Entry"
        verbose_name_plural = "Logbook Entries"

    def __str__(self):
        return f"Entry on {self.entry_date} - {self.weekly_log}"
