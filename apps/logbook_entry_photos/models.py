from django.db import models

from apps.core.models import BaseModel
from apps.logbook_entries.models import LogbookEntry


class LogbookEntryPhoto(BaseModel):
    photo = models.ImageField(upload_to='log_photos/')
    log_entry = models.ForeignKey(LogbookEntry, on_delete=models.CASCADE, related_name='photos')

    class Meta:
        verbose_name = "Logbook Entry Photo"
        verbose_name_plural = "Logbook Entry Photos"

    def __str__(self):
        return f"Photo for {self.log_entry}"