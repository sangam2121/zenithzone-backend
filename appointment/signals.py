from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from doctor.models import Doctor
from patient.models import Patient
from .models import Appointment, Payment


@receiver(post_save, sender=Payment)
def update_payment_status(sender, instance, created, **kwargs):
    if created:
        appointment = Appointment.objects.get(id=instance.appointment.id)
        appointment.payment_status = True
        appointment.status = 'approved'
        appointment.save()
