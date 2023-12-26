from django.db import models
from django.conf import settings

# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='patient/profiles', default='patient/images/default.png')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name_plural = 'Patients'
