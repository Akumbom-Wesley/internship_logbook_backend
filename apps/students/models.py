from django.db import models
from apps.core.models import BaseModel
from apps.departments.models import Department
from apps.users.models import User
from apps.utils.validations import validate_matricule_num

import os, base64, ecdsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from django.conf import settings

class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    matricule_num = models.CharField(max_length=10, validators=[validate_matricule_num])

    # We store the public key and encrypted private key
    public_key = models.TextField(blank=True)
    encrypted_private_key = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.matricule_num}"

    def set_private_key(self):
        """
        Generate ECDSA key pair, encrypt private key with server-held Fernet key,
        store encrypted private key and public key.
        """
        if self.encrypted_private_key:
            raise ValueError("Private key already exists. Cannot regenerate.")

        # Generate ECDSA key pair
        sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        private_key_hex = sk.to_string().hex()
        public_key_hex = sk.verifying_key.to_string().hex()
        self.public_key = public_key_hex

        # Encrypt private_key_hex with server Fernet key
        fernet_key = settings.FERNET_KEY.encode()  # should be base64 urlsafe key
        fernet = Fernet(fernet_key)
        encrypted = fernet.encrypt(private_key_hex.encode())
        self.encrypted_private_key = encrypted.decode()

        # Save model
        self.save()

    def get_private_key(self):
        """
        Decrypt and return the private key hex string using server Fernet key.
        """
        if not self.encrypted_private_key:
            raise ValueError("No encrypted private key stored.")
        fernet_key = settings.FERNET_KEY.encode()
        fernet = Fernet(fernet_key)
        decrypted = fernet.decrypt(self.encrypted_private_key.encode())
        return decrypted.decode()
