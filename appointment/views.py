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
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse


class AppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        doctor_id = self.request.GET.get('doctor_id')
        queryset = Appointment.objects.all()
        if doctor_id:
            queryset = queryset.filter(doctor__user__id=doctor_id)
        return queryset

class PatientAppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = PatientAppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Appointment.objects.all()
        date = self.request.GET.get('date')
        time = self.request.GET.get('time')
        doctor_id = self.request.GET.get('doctor_id')
        if time:
            queryset = queryset.filter(time_at=time)
        if date:
            queryset = queryset.filter(date=date)
        if doctor_id:
            try:
                doctor_id = CustomUser.objects.get(id=doctor_id).doctor.id
            except:
                doctor_id = None
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
            return JsonResponse({'error': 'User is not authenticated', 'status': f'{status.HTTP_401_UNAUTHORIZED}'}, status=status.HTTP_401_UNAUTHORIZED)
        payment = get_object_or_404(Payment, id=payment_id)
        appointment = Appointment.objects.filter(payment=payment)
        if not appointment.exists():
            return JsonResponse({'error': 'Appointment not found', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
        appointment = appointment.first()
        if appointment.payment.status == 'approved':
            return JsonResponse({'error': 'Payment has already been approved', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
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
        try:
            response = requests.request(
                "POST", url, headers=headers, data=json.dumps(payload))
            new_res = json.loads(response.text)
            print(new_res)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Payment could not be initiated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
        if new_res:
            try:
                payment = Payment.objects.get(purchase_order_id=purchase_order_id)
                payment.pidx = new_res['pidx']
                payment.save()
                return JsonResponse(new_res)
            except:
                if new_res['error_key'] is not None:
                    return JsonResponse(new_res['error_key'])




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
        serializer.save(doctor=doctor,payment=payment, patient=self.request.user.patient)
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            appointment = Appointment.objects.get(id=response.data['id'])
            payment = Payment.objects.get(appointment=appointment)
            response.data['payment'] = payment.id
            response.data['appointment'] = appointment.id
            return response
        except Exception as e:
            return Response({'error': 'Appointment could not be created: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

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

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Appointment updated successfully',
                'appointment': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Appointment could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDeleteView(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            response.data = {
                'message': 'Appointment deleted successfully',
                'appointment': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Appointment could not be deleted: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

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
            appointment = Appointment.objects.get(payment=payment)
            appointment.doctor.patient_checked += 1
            appointment.doctor.save()
            appointment.patient.appointment_count += 1
            appointment.patient.save()
            appointment.status = 'approved'
            appointment.save()
        return redirect('frontend')


class PaymentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.patient != self.request.user:
            raise PermissionError(
                'You are not allowed to update this payment'
            )

    def perform_destroy(self, instance):
        if instance.patient == self.request.user:
            instance.delete()
        else:
            raise PermissionError

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            response.data = {
                'message': 'Payment deleted successfully',
                'payment': response.data
            }
            return response
        except PermissionError as e:
            return Response({'error': 'You are not the owner of this payment.', 'status': f'{status.HTTP_403_FORBIDDEN}'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Payment could not be deleted: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class CompleteAppointmentView(APIView):
    def post(self, request, *args, **kwargs):
        appointment_id = request.data.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = 'completed'
        appointment.save()
        return Response({'message': 'Appointment completed successfully', 'status': f'{status.HTTP_200_OK}'}, status=status.HTTP_200_OK)

class RescheduleAppointmentView(APIView):
    def post(self, request, *args, **kwargs):
        appointment_id = request.data.get('appointment_id')
        new_date = request.data.get('new_date')
        new_time = request.data.get('new_time')
        if not new_date or not new_time:
            return Response({'error': 'New date and time must be provided', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
        # check if no appointment exists with the same doctor, date and time
        if (Appointment.objects.filter(doctor=appointment.doctor, date=new_date, time_at=new_time).exists()):
            return Response({'error': 'Appointment already exists', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.date = new_date
            appointment.time_at = new_time
            appointment.save()
        except:
            return Response({'error': 'Appointment could not be rescheduled', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
    ## inform the patient about the reschedule using email or sms
        return Response({'message': 'Appointment rescheduled successfully', 'status': f'{status.HTTP_200_OK}'}, status=status.HTTP_200_OK)