from django.shortcuts import render
from .serializers import AppointmentSerializer, PatientAppointmentSerializer, PaymentSerializer
from .models import Appointment, Payment
from rest_framework import generics, permissions
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        patient = self.request.user.patient
        serializer.save(patient=patient)


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


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # get the payment data
        appointment = Appointment.objects.get(id=self.kwargs['id'])
        serializer.save(appointment=appointment)

    def get_queryset(self):
        queryset = Payment.objects.all().filter(
            appointment__patient__user=self.request.user)
        return queryset


class PaymentUpdateRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Payment.objects.all().filter(
            appointment__patient__user=self.request.user)
        return queryset


class PaymentDeleteView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Payment.objects.all().filter(
            appointment__patient__user=self.request.user)
        return queryset
