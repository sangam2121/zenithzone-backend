from django.db.models.signals import post_save
from users.models import CustomUser
from django.dispatch import receiver

from .models import Doctor


@receiver(post_save, sender=CustomUser)
def create_doctor(sender, instance, created, **kwargs):
    print
    if created and instance.user_type.lower() == 'doctor':
        Doctor.objects.create(user=instance)
