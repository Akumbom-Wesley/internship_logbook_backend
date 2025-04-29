from django.db import models

from apps.core.models import BaseModel
from apps.users.models import User


class Notification(BaseModel):
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    users = models.ManyToManyField(User, related_name='notifications')

    def __str__(self):
        return self.title