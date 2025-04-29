from datetime import timedelta
from django.utils import timezone
from apps.supervisors.models import Supervisor


def delete_unapproved_supervisors():
    threshold = timezone.now() - timedelta(days=7)
    Supervisor.objects.filter(status='pending', created_at__lt=threshold).delete()