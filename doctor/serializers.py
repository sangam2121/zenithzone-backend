from rest_framework import serializers
from .models import Doctor, Clinic, Review, Location, Education, Experience
from users.serializers import CustomUserSerializer
from patient.models import Patient
from patient.serializers import PatientSerializer
from rest_framework.response import Response
from uuid import UUID


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
        validated_data.pop('patient')
        doctor = validated_data.pop('doctor')['user']
        patient = self.context['request'].user.patient
        review = Review.objects.create(patient=patient,doctor=doctor, **validated_data)
        return review


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "text", "location", "location_lat", "location_lon"]

# this is the doctor list serializer used to serialize doctor list in clinic
class DoctorListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    # clinic =ClinicSerializer()

    class Meta:
        model = Doctor
        fields = ["user", "speciality", "image", "reviews", "appointment_fee", "patient_checked"]
        depth = 1

# this is the clinic serializer
class ClinicSerializer(serializers.ModelSerializer):
    doctors = DoctorListSerializer(many=True, read_only=True)   
    address = LocationSerializer()
    class Meta:
        model = Clinic
        fields = ["id", "name", "address", "phone", "doctors"]

# secondary clinic serializer, supposed to be used to serialize clinic for doctor list
class ClinicDoctorSerializer(serializers.ModelSerializer):
    address = LocationSerializer()
    class Meta:
        model = Clinic
        fields = ["id", "name", "address", "phone"]


class EducationSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor.user.id', allow_null=True, required=False)

    class Meta:
        model = Education
        fields = ["id", "doctor", "level", "school", "major", "start_date", "end_date"]
        depth = 1

    def create(self, validated_data):
        validated_data.pop('doctor')
        doctor = self.context['request'].user.doctor
        print(doctor)
        education = Education.objects.create(doctor=doctor, **validated_data)
        return education

class ExperienceSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor.user.id', allow_null=True, required=False)

    class Meta:
        model = Experience
        fields = ["id", "doctor", "title", "hospital", "start_date", "end_date"]
        depth = 1

    def create(self, validated_data):
        validated_data.pop('doctor')
        doctor = self.context['request'].user.doctor
        print(doctor)
        experience = Experience.objects.create(doctor=doctor, **validated_data)
        return experience
class DoctorSerializer(serializers.ModelSerializer):
    # pk = serializers.CharField(source='user.pk', read_only=True)
    user = CustomUserSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    clinic = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(), source='clinic.id', allow_null=True, required=False)
    education = EducationSerializer(many=True, read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = ["id","user", "speciality", "image", "reviews", "clinic", "appointment_fee", "patient_checked", "education", "experience"]
        depth = 1

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user')
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.phone = user_data.get('phone', user.phone)
        user.address = user_data.get('address', user.address)
        user.save()
        clinic_data = validated_data.pop('clinic')
        clinic = instance.clinic
        clinic.name = clinic_data.get('name', clinic.name)
        clinic.save()
        instance.speciality = validated_data.get('speciality', instance.speciality)
        instance.image = validated_data.get('image', instance.image)
        instance.appointment_fee = validated_data.get('appointment_fee', instance.appointment_fee)
        instance.save()
        return instance
      
