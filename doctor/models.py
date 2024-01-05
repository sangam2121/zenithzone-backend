from django.db import models
from django.conf import settings
from patient.models import Patient
import uuid
# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(
        upload_to='doctor/profiles', default='doctor/images/default.png')
    clinic = models.ForeignKey(
        "Clinic", on_delete=models.CASCADE, null=True, blank=True)
    appointment_fee = models.IntegerField(default=0)

    @property
    def get_rating(self):
        reviews = self.reviews.all()
        if len(reviews) > 0:
            total = 0
            for review in reviews:
                total += review.rating
            return total / len(reviews)
        else:
            return 0

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name_plural = 'Doctors'
        # order by rating
        ordering = ['-reviews__rating']


class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Clinics'
        ordering = ['name']


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='reviews')
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doctor.user.first_name + "_" + self.patient.user.first_name + ": " + str(self.rating)

    class Meta:
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
