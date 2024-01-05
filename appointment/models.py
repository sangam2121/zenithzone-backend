from django.db import models
import uuid
from doctor.models import Doctor
from patient.models import Patient

# Create your models here.
appointment_status = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('completed', 'Completed'),
)


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(
        "doctor.Doctor", on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(
        "patient.Patient", on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField(format('%H:%M'))
    payment_status = models.BooleanField(default=False)
    status = models.CharField(
        max_length=100, choices=appointment_status, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doctor.user.first_name + "_" + self.patient.user.first_name + ": " + self.status

    class Meta:
        verbose_name_plural = 'Appointments'
        ordering = ['-created_at']
        unique_together = ('doctor', 'date', 'time')

    @property
    def get_patient_name(self):
        return self.patient.user.first_name + ' ' + self.patient.user.last_name

    @property
    def get_status(self):
        return self.status

    @property
    def reject(self):
        self.status = 'rejected'
        self.save()

    @property
    def approve(self):
        self.status = 'approved'
        self.save()

    @property
    def complete(self):
        self.status = 'completed'
        self.save()


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name='payment')
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.appointment.doctor.user.first_name + "_" + self.appointment.patient.user.first_name + ": " + str(self.amount)

    class Meta:
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']

    def save(self, *args, **kwargs):
        if self.amount < self.appointment.doctor.appointment_fee:
            raise ValueError(
                'Payment amount cannot be less than appointment fee')
        super(Payment, self).save(*args, **kwargs)
