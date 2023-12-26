from django.db.models.signals import post_save, post_delete
from users.models import CustomUser
from django.dispatch import receiver

from .models import Doctor


@receiver(post_save, sender=CustomUser)
def create_doctor(sender, instance, created, **kwargs):
    print
    if created and instance.user_type.lower() == 'doctor':
        Doctor.objects.create(user=instance)


@receiver(post_delete, sender=Doctor)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
