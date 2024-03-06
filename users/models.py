from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid
from django.contrib.auth.hashers import make_password



class CustomUserManager(BaseUserManager):
    def create_user(self, email,user_type, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        print(user_type)
        if not user_type:
            raise ValueError('The user_type field must be set')
        user = self.model(user_type=user_type,email=email, **extra_fields)
        user.set_password(password)
        print("From user manager")
        print(make_password(password))
        user.save()
        return user

    def create_superuser(self, email ,user_type, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Super User must have staff permission!")
        print(user_type)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Super User must have superuser permission!")
        return self.create_user(email, user_type, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=[(
        'doctor', 'Doctor'), ('patient', 'Patient'), ('admin', 'Admin')])

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type','first_name', 'last_name']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.user_type == 'doctor':
            self.is_staff = True
        if self.user_type == 'admin':
            self.is_superuser = True
            self.is_staff = True
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    @property
    def is_doctor(self):
        return self.user_type == 'doctor'

    @property
    def is_patient(self):
        return self.user_type == 'patient'

    @property
    def is_admin(self):
        return self.user_type == 'admin'
