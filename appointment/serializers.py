from rest_framework import serializers
from .models import Appointment
from doctor.models import Doctor
from patient.models import Patient


class PatientAppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor.user')
    patient = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(), source='patient.user')
    time = serializers.TimeField(format="%H:%M")
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time']

    def create(self, validated_data):
        # status = 'pending'
        # validated_data['status'] = status
        return Appointment.objects.create(**validated_data)


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor.user')
    patient = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(), source='patient.user')
    time = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time']

    def create(self, validated_data):
        # status = 'pending'
        # validated_data['status'] = status
        return Appointment.objects.create(**validated_data)
