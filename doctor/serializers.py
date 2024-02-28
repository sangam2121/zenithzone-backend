from rest_framework import serializers
from .models import Doctor, Clinic, Review, Location
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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "text", "location", "location_lat", "location_lon"]


class DoctorListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    reviews = ReviewSerializer(many=True)
    # clinic =ClinicSerializer()

    class Meta:
        model = Doctor
        fields = ["user", "speciality", "image", "reviews"]
        depth = 1


class ClinicSerializer(serializers.ModelSerializer):
    doctors = DoctorListSerializer(many=True, read_only=True)   
    address = LocationSerializer()
    class Meta:
        model = Clinic
        fields = ["id", "name", "address", "phone", "doctors"]

class DoctorSerializer(serializers.ModelSerializer):
    # pk = serializers.CharField(source='user.pk', read_only=True)
    user = CustomUserSerializer()
    reviews = ReviewSerializer(many=True)
    clinic = ClinicSerializer()

    class Meta:
        model = Doctor
        fields = ["id","user", "speciality", "image", "reviews", "clinic"]
        depth = 1