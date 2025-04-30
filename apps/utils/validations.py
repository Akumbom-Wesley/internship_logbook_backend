import re

from django.core.exceptions import ValidationError


def validate_matricule_num(value):
    """
    Validates the format of the matricule number.
    Expected format: UBa[2-digit year][A-Z][4-digit number] (e.g., UBa25E0001)
    """
    pattern = r'^UBa\d{2}[A-Z]\d{4}$'
    if not re.match(pattern, value):
        raise ValidationError(
            "Invalid matricule number format."
        )


def validate_contact(value):
    pattern = r'^\+2376[245789]\d{7}$'
    if not re.match(pattern, value):
        raise ValidationError("Invalid contact number format. Must be in the format +2376[245789]XXXXXXX"
                              " (e.g., +237 623 456 789).")