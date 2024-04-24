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
    print("Hello here")
    if not created:
        print("Hello here2")
        if instance.status == 'approved':
            print("Hello here3")
            doctor = instance.doctor
            patient_name = instance.patient.user.first_name.title() + ' ' + instance.patient.user.last_name.title()
            from_email =  settings.EMAIL_HOST_USER
            to_email = doctor.user.email
            subject = f'Your Appointment with {patient_name} on {instance.date} Has Been Scheduled'
            message = f"Hello! Your appointment with {patient_name} has been successfully scheduled. It will take place on {instance.date} at {instance.time}. Please let us know if you need to make any changes. We look forward to seeing you!"
            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )


@receiver(post_save, sender=Appointment)
def notice_to_patient(sender, instance, created, **kwargs):
    print("Hello here")
    if not created:
        print("Hello here2")
        if instance.status == 'approved':
            print("Hello here3")
            patient = instance.patient
            patient_name = patient.user.first_name.title() + ' ' + patient.user.last_name.title()
            from_email =  settings.EMAIL_HOST_USER
            to_email = patient.user.email
            subject = f"Good News, {patient_name}! Your Appointment on {instance.date} Has Been Approved"
            message = f"Good news! Your appointment with Dr. {instance.doctor.user.last_name} ({instance.doctor.user.email}) has been confirmed. The appointment is scheduled for {instance.date} at {instance.time}. We look forward to seeing you then!"
            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )