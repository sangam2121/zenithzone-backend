from django.db import models
from django.conf import settings
# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(
        upload_to='doctor/profiles', default='doctor/images/default.png')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Doctors'


class Clinic(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='clinics')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Clinics'
