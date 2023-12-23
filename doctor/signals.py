from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Doctor


@receiver(post_save, sender=User)
def create_doctor(sender, instance, created, **kwargs):
    if created and user.user_type == 'doctor':
        Doctor.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)
