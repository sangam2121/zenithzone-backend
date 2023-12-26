from django.db.models.signals import post_save
from users.models import CustomUser
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_patient(sender, instance, created, **kwargs):
    if created:
        if instance.user_type.lower() == 'patient':
            from patient.models import Patient
            Patient.objects.create(user=instance)
