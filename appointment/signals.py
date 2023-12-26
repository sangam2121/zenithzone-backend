from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from doctor.models import Doctor
from patient.models import Patient
from .models import Appointment
