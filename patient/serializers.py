from rest_framework import serializers
from users.serializers import CustomUserSerializer
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Patient
        fields = ['id','image', 'user']

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
            user.save()
        except:
            pass
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
