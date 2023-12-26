from rest_framework import serializers


class PatientSerializer(serializers.Serializer):
    class Meta:
        model = Patient
        fields = '__all__'
