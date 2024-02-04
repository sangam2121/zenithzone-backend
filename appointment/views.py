from django.shortcuts import render
from .serializers import AppointmentSerializer, PatientAppointmentSerializer
from .models import Appointment
from rest_framework import generics, permissions
import json
from decouple import config
from doctor.models import Doctor
import requests
from rest_framework import serializers
# Create your views here.


class AppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Appointment.objects.all().filter(
            doctor__user=self.request.user)
        return queryset


class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        doctor_id = self.request.data.get('doctor')
        doctor = Doctor.objects.get(id=doctor_id)
        appointment_fee = doctor.appointment_fee
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        payload = json.dumps(self.request.data)
        headers = {
            'Authorization': 'key' + config('KHALTI_SECRET'),
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            # Verify the payment
            url = "https://a.khalti.com/api/v2/epayment/lookup/"
            pidx = response.json().get('pidx')
            data = json.dumps({
                'pidx': pidx
            })
            res = requests.request('POST', url, headers=headers, data=data)
            new_res = json.loads(res.text)

            if new_res['status'] == 'Completed' and new_res['amount'] == appointment_fee:
                # If payment is verified, create the appointment
                patient = self.request.user.patient
                serializer.save(patient=patient)
            else:
                # If payment is not verified, return an error response
                raise serializers.ValidationError(
                    "Payment verification failed or insufficient amount.")
        else:
            # If payment initiation failed, return an error response
            raise serializers.ValidationError("Payment initiation failed.")


class AppointmentUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    # serializer modified to allow partial update
    def get_serializer(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_doctor:
            self.serializer_class = AppointmentSerializer
        else:
            self.serializer_class = PatientAppointmentSerializer

        return super(AppointmentUpdateView, self).get_serializer(*args, **kwargs)


# class PaymentListCreateView(generics.ListCreateAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         # get the payment data
#         appointment = Appointment.objects.get(id=self.kwargs['id'])
#         serializer.save(appointment=appointment)

#     def get_queryset(self):
#         queryset = Payment.objects.all().filter(
#             appointment__patient__user=self.request.user)
#         return queryset


# class PaymentUpdateRetrieveView(generics.RetrieveUpdateAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     lookup_field = 'id'

#     def get_queryset(self):
#         queryset = Payment.objects.all().filter(
#             appointment__patient__user=self.request.user)
#         return queryset


# class PaymentDeleteView(generics.DestroyAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     lookup_field = 'id'

#     def get_queryset(self):
#         queryset = Payment.objects.all().filter(
#             appointment__patient__user=self.request.user)
#         return queryset
