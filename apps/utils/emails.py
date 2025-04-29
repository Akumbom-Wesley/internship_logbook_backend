from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def send_verification_email(supervisor, request):
    verification_link = request.build_absolute_uri(
        reverse('verify-supervisor', kwargs={'supervisor_id': str(supervisor.id)})
    )
    subject = "Verify Supervisor Account"
    message = f"Click the link to verify: {verification_link}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [supervisor.company.email], fail_silently=False)