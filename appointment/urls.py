from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

def go_to_front_end(request):
    return redirect('http://localhost:5173/')

# app_name = 'appointment'
urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='create-appointment'),
    path('lists/', AppointmentListView.as_view(), name='list'),
    path('update/<slug:id>/', AppointmentUpdateView.as_view(), name='update'),
    path('pay/', InitPaymentView.as_view(), name='initiate-payment'),
    path('callback/', PaymentCallbackView.as_view(), name='callback'),
    path('doctor/<slug:doctor_id>/', AppointmentListView.as_view(), name='doctor-appointment-list'),
    path('payment/details/<slug:pk>/', PaymentUpdateDeleteView.as_view(), name='payment-details'),
    path('delete/<slug:pk>/', AppointmentDeleteView.as_view(), name='delete'),
    path('front-end/', go_to_front_end, name='front-end'),
    path('complete/<slug:pk>/', CompleteAppointmentView.as_view(), name='complete-appointment'),
    path('reschedule/', RescheduleAppointmentView.as_view(), name='reschedule-appointment'),
]
