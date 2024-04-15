from django.db import models
from django.conf import settings
from patient.models import Patient
import uuid
# Create your models here.



class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor")
    speciality = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(
        upload_to='doctor/profiles', default='default.png')
    clinic_name = models.CharField(max_length=100, null=True, blank=True)
    clinic_address_lon = models.FloatField(null=True, blank=True)
    clinic_address_lat = models.FloatField(null=True, blank=True)
    appointment_fee = models.IntegerField(default=0)
    patient_checked = models.PositiveIntegerField(default=0)

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
        return str(self.user.id)

    class Meta:
        verbose_name_plural = 'Doctors'
        # order by rating
        ordering = ['-reviews__rating']




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

    def save(self, *args, **kwargs):
        # check if the patient has already reviewed the doctor
        if self.patient.reviews.filter(doctor=self.doctor).exists():
            raise ValueError('You have already reviewed this doctor!')
        # check if the patient has already booked an appointment with the doctor
        if not self.patient.appointments.filter(doctor=self.doctor).exists():
            raise ValueError('You have not booked an appointment with this doctor!')
        appointments = self.patient.appointments.filter(doctor=self.doctor)
        # check if the patient has completed the appointment with the doctor
        print(appointments)
        if not self.patient.appointments.filter(doctor=self.doctor, status='completed').exists():
            print('here')
            raise ValueError('You have not completed the appointment with this doctor!')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

education_level = [
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('phd', 'PhD')
]
class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='education')
    level = models.CharField(max_length=10, choices=education_level, default='bachelor')
    school = models.CharField(max_length=100)
    major = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.doctor.user.first_name + "_" + self.school

    class Meta:
        verbose_name_plural = 'Educations'
        ordering = ['-end_date']
        unique_together = ['doctor', 'school', 'level']

class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='experience')
    title = models.CharField(max_length=100)
    hospital = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.doctor.user.first_name + "_" + self.title

    class Meta:
        verbose_name_plural = 'Experiences'
        ordering = ['-end_date']
        unique_together = ['doctor', 'hospital', 'title']