from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.db import models

from apps.core.models import BaseModel
from apps.utils.validations import validate_contact


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Set default values for required fields
        extra_fields.setdefault('full_name', email.split('@')[0])
        extra_fields.setdefault('role', 'super-admin')
        extra_fields.setdefault('contact', '670928637')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('supervisor', 'Supervisor'),
        ('super_admin', 'Super Admin')
    ]

    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    contact = models.CharField(max_length=15, validators=[validate_contact])
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')

    # Required fields for AbstractBaseUser
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [models.Index(fields=['email'])]

    # required for Django's admin
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email

    objects = UserManager()

    USERNAME_FIELD = 'email'
