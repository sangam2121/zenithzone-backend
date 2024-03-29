from rest_framework import serializers
from users.serializers import CustomUserSerializer
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=False)

    class Meta:
        model = Patient
        fields = ['id','image', 'user', 'created_at', 'appointment_count']

    def create(self, validated_data):
        user = self.context['request'].user
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

    def update(self, instance, validated_data):
        try:
            user_data = validated_data.pop('user')
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.phone = user_data.get('phone', user.phone)
            user.address = user_data.get('address', user.address)
            user.bio = user_data.get('bio', user.bio)
            user.save()
        except KeyError:
            pass
        instance.image = validated_data.get('image', instance.image)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance
