from django.db import models
from django.conf import settings

# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='patient/profiles', default='default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    appointment_count = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name_plural = 'Patients'
        ordering = ['-user__first_name']
