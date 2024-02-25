from django.db import models
import uuid
from doctor.models import Doctor
from patient.models import Patient
from users.models import CustomUser


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(
        "doctor.Doctor", on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(
        "patient.Patient", on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField(format('%H:%M'))
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doctor.user.first_name + "_" + self.patient.user.first_name + ": " + self.payment.status

    class Meta:
        verbose_name_plural = 'Appointments'
        ordering = ['-created_at']
        unique_together = ('doctor', 'date', 'time')

    @property
    def get_patient_name(self):
        return self.patient.user.first_name + ' ' + self.patient.user.last_name


payment_status = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('completed', 'Completed'),
)




class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=payment_status, default='pending')
    pidx = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    purchase_order_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + ": " + self.status + "( " + str(self.pidx) + " )"


