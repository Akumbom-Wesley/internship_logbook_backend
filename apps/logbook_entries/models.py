from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from apps.core.models import BaseModel
from apps.weekly_logs.models import WeeklyLog
import ecdsa  # Modern cryptographic library for digital signatures
from django.conf import settings


class LogbookEntryManager(models.Manager):
    def immutable(self):
        return self.filter(is_immutable=True)


class LogbookEntry(BaseModel):
    description = models.TextField(max_length=1000)
    is_immutable = models.BooleanField(default=False)
    feedback = models.TextField(max_length=500, blank=True)
    signature = models.TextField(blank=True)       # latest signature
    original_signature = models.TextField(blank=True, null=True)

    weekly_log = models.ForeignKey(WeeklyLog, on_delete=models.CASCADE, related_name='logbook_entries')

    objects = LogbookEntryManager()

    def clean(self):
        if not self.description:
            raise ValidationError("Description cannot be empty.")
        if self.is_immutable and not self.signature:
            raise ValidationError("A digital signature is required for immutable entries.")

    def generate_signature(self, user_private_key_hex):
        # Sign description+feedback+timestamp
        message = f"{self.description}{self.feedback}{self.created_at.isoformat()}".encode()
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(user_private_key_hex), curve=ecdsa.NIST256p)
        signature = sk.sign(message).hex()
        return signature

    def verify_signature(self, signature_hex):
        student = self.weekly_log.logbook.internship.student
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(student.public_key), curve=ecdsa.NIST256p)
        message = f"{self.description}{self.feedback}{self.created_at.isoformat()}".encode()
        try:
            return vk.verify(bytes.fromhex(signature_hex), message)
        except Exception:
            return False

    def save(self, *args, **kwargs):
        self.clean()

        # Only generate signature if this is a new instance and not already signed
        if not self.pk and hasattr(self.weekly_log.logbook.internship.student, 'encrypted_private_key'):
            # Save first to get created_at populated
            super().save(*args, **kwargs)

            student = self.weekly_log.logbook.internship.student
            try:
                private_key = student.get_private_key()  # implement secure access
                self.signature = self.generate_signature(private_key)
                self.original_signature = self.signature
            except Exception as e:
                raise ValidationError(f"Failed to generate signature: {e}")

            # Save again with signature
            return super().save(update_fields=['signature', 'original_signature'])

        # Regular update (or already has pk)
        return super().save(*args, **kwargs)

    def __str__(self):
        status = "approved" if self.is_immutable else "pending_approval"
        return f"Entry on {self.created_at.date()} - Week {self.weekly_log.week_no} - user {self.weekly_log.logbook.internship.student.user.id} - {status}"