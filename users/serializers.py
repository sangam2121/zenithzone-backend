from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import CustomUser as User
from patient.models import Patient
from doctor.models import Doctor


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['user_id'] = str(user.id)
        token['user_name'] = user.first_name + ' ' + user.last_name
        token['user_type'] = user.user_type
        token['image'] = user.doctor.image.url if user.user_type == 'doctor' else user.patient.image.url if user.user_type == 'patient' else None
        return token

    class Meta:
        model = User
        fields = ('email', 'password')

 

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True,
         required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    user_type = serializers.ChoiceField(
        choices=[('doctor', 'Doctor'), ('patient', 'Patient'), ('admin', 'Admin')])

    class Meta:
        model = User
        fields = ('email', 'password', 'password2',
                  'user_type', 'first_name', 'last_name', 'phone', 'address', 'bio')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_type': {'required': True},
        }


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type'],
            phone=validated_data['phone'],
            address=validated_data['address'],
        )

        user.set_password(validated_data['password'])
        print(validate_password(validated_data['password'], user))
        print(user)
        print(make_password(validated_data['password']))
        print(validated_data['password'])
        user.save()

        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'user_type', 'phone', 'address', 'bio')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_type': {'required': True},
        }
        read_only_fields = ('id', 'email', 'user_type')
        depth = 1


class DoctorAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'image', 'user']

class PatientAuthorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'image', 'user']

class UserAuthorSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 
                  'image')

    def get_image(self, obj):
        if obj.user_type == 'doctor':
            return DoctorAuthorSerializer(obj.doctor).data['image']
        elif obj.user_type == 'patient':
            return PatientAuthorSerializer(obj.patient).data['image']
        else:
            return None

    