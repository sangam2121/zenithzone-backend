from rest_framework import serializers
from .models import Appointment, Payment
from doctor.models import Doctor
from patient.models import Patient
from doctor.serializers import DoctorListSerializer
from patient.serializers import PatientSerializer



class PatientAppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor.user')
    patient = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(), source='patient.user')
    # time = serializers.TimeField(format="%H:%M")
    # status = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time_at', 'payment']
        read_only_fields = ['payment']

    def create(self, validated_data):
        # status = 'pending'
        # validated_data['status'] = status
        return Appointment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.time_at = validated_data.get('time_at', instance.time_at)
        instance.save()
        return instance



class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor.user')
    patient = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(), source='patient.user')
    # time = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date',  'time_at', 'payment']
        read_only_fields = ['payment']

    def create(self, validated_data):
        # status = 'pending'
        # validated_data['status'] = status
        # check if there is any other appointment with the same doctor, date and time (+- 3 hour)
        # if yes, raise serializers.ValidationError("Appointment already exists")
        # else, create the appointment
        return Appointment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.time_at = validated_data.get('time_at', instance.time_at)
        instance.save()
        return instance

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user',
                  'amount', 'status', 'pidx', 'transaction_id', 'purchase_order_id']
        depth = 1

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.transaction_id = validated_data.get(
            'transaction_id', instance.transaction_id)
        instance.save()
        return instance

class AppointmentListSerializer(serializers.ModelSerializer):
    doctor = DoctorListSerializer()
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time_at', 'status', 'payment']
        depth = 1