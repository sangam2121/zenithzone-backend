from rest_framework import serializers
from .models import Doctor, Clinic, Review
from users.serializers import CustomUserSerializer
from patient.models import Patient


class ReviewSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor.user')
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source='patient.user')

    class Meta:
        model = Review
        fields = ["id", "doctor", "patient", "comment", "rating"]
        depth = 1

    def create(self, validated_data):
        patient = self.context['request'].user.patient
        review = Review.objects.create(patient=patient, **validated_data)
        return review


class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    reviews = ReviewSerializer(many=True)
    clinic = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all())

    class Meta:
        model = Doctor
        fields = ["user", "speciality", "image", "reviews", "clinic"]
        depth = 1


class ClinicSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer(many=True, read_only=True)

    class Meta:
        model = Clinic
        fields = ["id", "name", "address", "phone", "doctors"]
