from rest_framework import serializers
from users.serializers import CustomUserSerializer
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Patient
        fields = ['image', 'user']
