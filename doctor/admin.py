from django.contrib import admin
from .models import Doctor, Clinic, Review, Education, Experience 

class DoctorList(admin.ModelAdmin):
    list_display = ('user', 'speciality', 'appointment_fee', 'patient_checked')
    search_fields = ('user', 'speciality', 'appointment_fee', 'patient_checked')
    list_filter = ('speciality', 'appointment_fee', 'patient_checked')
    ordering = ('speciality', 'appointment_fee', 'patient_checked')


# Register your models here.
admin.site.register(Clinic)
admin.site.register(Review)
admin.site.register(Education)
admin.site.register(Experience)


admin.site.register(Doctor, DoctorList)