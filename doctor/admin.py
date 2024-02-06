from django.contrib import admin
from .models import Doctor, Clinic, Review, Location


# Register your models here.
admin.site.register(Doctor)
admin.site.register(Clinic)
admin.site.register(Review)
admin.site.register(Location)
