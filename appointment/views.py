from django.shortcuts import render, get_object_or_404, redirect
from .serializers import AppointmentSerializer, PatientAppointmentSerializer
from .models import Appointment
from rest_framework import generics, permissions
import json
from decouple import config
from users.models import CustomUser
import requests
from rest_framework import serializers
# Create your views here.
import uuid
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# login required
from django.contrib.auth.decorators import login_required


class AppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Appointment.objects.all().filter(
            doctor__user=self.request.user)
        return queryset


class InitPaymentView(View):
    authentication_classes = ()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InitPaymentView, self).dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    # @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        doctor_id = self.request.POST.get('doctor')
        user = get_object_or_404(CustomUser, id=doctor_id)
        appointment_fee = user.doctor.appointment_fee
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        return_url = "https://127.0.0.1:8000/api" + \
            reverse('create-appointment')
        purchase_order_id = str(uuid.uuid4())
        purchase_order_name = "Appointment Fee"

        # name = request.user.first_name + \
        #     " " + request.user.last_name
        # email = request.user.email
        # phone = request.user.phone
        name = "Ram"
        email = "ram@email.com"
        phone = "9841234567"
        payload = {
            "return_url": return_url,
            "website_url": return_url,
            "public_key": config('KHALTI_PUBLIC'),
            "amount": appointment_fee,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_order_name,
            "customer_info": {
                "name": name,
                "email": email,
                "phone": phone
            }
        }
        print(payload)

        headers = {
            'Authorization': 'key' + " " + config('KHALTI_SECRET'),
            'Content-Type': 'application/json',
        }
        print(headers)
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))
        new_res = json.loads(response.text)
        print(new_res)
        # if no new_res, return an error response
        if new_res is None:
            raise serializers.ValidationError("Payment initiation failed.")
        return redirect(new_res['payment_url'])

# @csrf_exempt
# def init_payment(request):
#     if request.method == 'POST':
#         doctor_id = request.POST.get('doctor')
#         print(request.POST)
#         user = get_object_or_404(CustomUser, id=doctor_id)
#         appointment_fee = user.doctor.appointment_fee
#         url = "https://khalti.com/api/v2/payment/initiate/"
#         return_url = reverse('create-appointment')
#         purchase_order_id = str(uuid.uuid4())
#         purchase_order_name = "Appointment Fee"
#         name = request.user.first_name + \
#             " " + request.user.last_name
#         email = request.user.email
#         phone = request.user.phone
#         payload = {
#             "public_key": config('KHALTI_PUBLIC'),
#             "amount": appointment_fee,
#             "purchase_order_id": purchase_order_id,
#             "purchase_order_name": purchase_order_name,
#             "customer_info": {
#                 "name": name,
#                 "email": email,
#                 "phone": phone
#             }
#         }

#         headers = {
#             'Authorization': 'key' + config('KHALTI_SECRET'),
#             'Content-Type': 'application/json',
#         }
#         response = requests.request(
#             "POST", url, headers=headers, data=json.dumps(payload))
#         new_res = json.loads(response.text)

#         return redirect(new_res['payment_url'])


class AppointmentCreateView(generics.CreateAPIView):
    # verify payment
    # if verified, create appointment

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        doctor = Doctor.objects.get(id=self.request.data.get('doctor'))
        appointment_fee = doctor.appointment_fee
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        pidx = self.request.data.get('pidx')
        # if no pidx, return an error response
        if pidx is None:
            raise serializers.ValidationError("Payment initiation failed.")
        data = json.dumps({
            'pidx': pidx
        })
        headers = {
            'Authorization': 'key' + config('KHALTI_SECRET'),
            'Content-Type': 'application/json',
        }
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


class AppointmentUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
