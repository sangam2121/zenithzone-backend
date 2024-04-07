from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import CustomUser
from doctor.models import Doctor
from patient.models import Patient
from .models import Appointment, Payment
from django.core.mail import send_mail
from django.conf import settings




@receiver(post_delete, sender=Appointment)
def delete_payment(sender, instance, **kwargs):
    try:
        instance.payment.delete()
    except:
        pass


@receiver(post_delete, sender=Payment)
def delete_appointment(sender, instance, **kwargs):
    if instance.appointment_set:
        for appointment in instance.appointment_set.all():
            appointment.delete()

@receiver(post_save, sender=Appointment)
def notice_to_doctor(sender, instance, created, **kwargs):
    if created:
        doctor = instance.doctor
        from_email =  settings.EMAIL_HOST_USER
        to_email = doctor.user.email
        subject = f'New Appointment'
        message = f'You have a new appointment from {instance.patient.user.email} on {instance.date} at {instance.time}.'
        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False,
        )


@receiver(post_save, sender=Appointment)
def notice_to_patient(sender, instance, created, **kwargs):
    if created:
        patient = instance.patient
        from_email =  settings.EMAIL_HOST_USER
        to_email = patient.user.email
        subject = f'New Appointment'
        message = f'Your appointment with {instance.doctor.user.email} on {instance.date} at {instance.time} has been scheduled.'
        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False,
        )
