from rest_framework import serializers
from .models import Doctor
from users.serializers import CustomUserSerializer


class DoctorSerializer(serializers.Serializer):
    user = CustomUserSerializer()
    speciality = serializers.CharField(max_length=100)
    image = serializers.ImageField()

    class Meta:
        model = Doctor
        fields = ["user", "speciality", "image"]
        depth = 1
