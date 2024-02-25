from django.db.models.signals import post_save
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
