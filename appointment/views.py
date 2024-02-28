from django.shortcuts import render, get_object_or_404, redirect
from .serializers import AppointmentSerializer, PatientAppointmentSerializer
from .models import Appointment, Payment
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
# json web token
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework import exceptions
from rest_framework import authentication
import jwt
from doctor.models import Doctor
from patient.models import Patient
from rest_framework.response import Response
from rest_framework.decorators import api_view

class AppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Appointment.objects.all().filter(
            doctor__user=self.request.user)
        return queryset

class PatientAppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = PatientAppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Appointment.objects.all().filter(
            patient__user=self.request.user)
        date = self.request.GET.get('date')
        time = self.request.GET.get('time')
        doctor_id = self.request.GET.get('doctor_id')
        if time:
            queryset = queryset.filter(time_at=time)
        if date:
            queryset = queryset.filter(date=date)
        if doctor_id:
            doctor_id = CustomUser.objects.get(id=doctor_id).doctor.id
            queryset = queryset.filter(doctor__id=doctor_id)
        return queryset



class InitPaymentView(View):
    authentication_classes = (JWTAuthentication)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

    # @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        JWT_authenticator = JWTAuthentication()

        # authenitcate() verifies and decode the token
        # if token is invalid, it raises an exception and returns 401
        response = JWT_authenticator.authenticate(request)
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        payment_id = body_data.get('payment_id')
        redirect_url = body_data.get('redirect_url')
        # print(payment_id)
        if response is not None:
            # unpacking
            user, token = response
            # print("this is decoded token claims", token.payload)
        else:
            print("no token is provided in the header or the header is missing")
        payment = get_object_or_404(Payment, id=payment_id)
        purchase_order_id = payment.purchase_order_id
        purchase_order_name = "Appointment Fee"
        appointment_fee = payment.amount
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        return_url = "http://127.0.0.1:8000/" + \
            reverse('callback')
        name = user.first_name + " " + user.last_name
        email = user.email
        phone = user.phone
        if phone == None or phone == "":
            phone = "9800000000"
        payload = {
            "return_url": return_url,
            "website_url": redirect_url,
            "public_key": config('KHALTI_PUBLIC'),
            "amount": str(appointment_fee * 100),
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_order_name,
            "customer_info": {
                "name": name,
                "email": email,
                "phone": phone
            }
        }
        headers = {
            'Authorization': 'key' + " " + config('KHALTI_SECRET'),
            'Content-Type': 'application/json',
        }
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))
        new_res = json.loads(response.text)
        # print(new_res)
        if new_res:
            try:
                payment = Payment.objects.get(purchase_order_id=purchase_order_id)
                payment.pidx = new_res['pidx']
                payment.save()
                return redirect(new_res['payment_url'])
            except:
                if new_res['error_key'] is not None:
                    raise serializers.ValidationError(
                        "Payment initiation failed." + new_res['error_key'])




class AppointmentCreateView(generics.CreateAPIView):
    # verify payment
    # if verified, create appointment

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        # create a appointment and a payment object with status pending
        data = self.request.data
        doctor_id = self.request.data.get('doctor')
        print(doctor_id)
        doctor = Doctor.objects.get(id=doctor_id)
        appointment_fee = doctor.appointment_fee
        purchase_order_id = str(uuid.uuid4())
        purchase_order_name = "Appointment Fee"
        payment = Payment.objects.create(
            user=self.request.user,
            amount=appointment_fee,
            status='pending',
            purchase_order_id = purchase_order_id
        )
        # print(payment)
        # print(self.request.user.patient)
        serializer.save(payment=payment, doctor=doctor, patient=self.request.user.patient)
        # print(serializer.data)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        appointment = Appointment.objects.get(id=response.data['id'])
        payment = Payment.objects.get(appointment=appointment)
        response.data['payment'] = payment.id
        response.data['appointment'] = appointment.id
        return response

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


class PaymentCallbackView(View):
    def get(self, request, *args, **kwargs):
        transaction_id = request.GET.get('transaction_id')
        pidx = request.GET.get('pidx')
        # update the Payment object with transaction_id and status
        amount = request.GET.get('amount')
        payment = Payment.objects.get(pidx=pidx)
        if payment:
            payment.transaction_id = transaction_id
            payment.status = 'approved'
            payment.save()
        return redirect('create-appointment')
