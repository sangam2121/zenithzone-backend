from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import CustomUser
from doctor.models import Doctor
from patient.models import Patient
from .models import Appointment, Payment


# @receiver(post_save, sender=Payment)
# def update_appointment_payment_status(sender, instance, created, **kwargs):
#     if instance.status == 'approved':
#         instance.payment_status = True
#         instance.appointment.save()
#     elif instance.status == 'rejected':
#         instance.appointment.payment_status = False
#         instance.appointment.save()


@receiver(post_delete, sender=Appointment)
def delete_payment(sender, instance, **kwargs):
    if instance.payment:
        instance.payment.delete()

@receiver(post_delete, sender=Payment)
def delete_appointment(sender, instance, **kwargs):
    if instance.appointment:
        instance.appointment.delete()