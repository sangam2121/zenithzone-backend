from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

# app_name = 'appointment'
urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='create-appointment'),
    path('lists/', AppointmentListView.as_view(), name='list'),
    path('update/<slug:id>/', AppointmentUpdateView.as_view(), name='update'),
    path('pay/', InitPaymentView.as_view(), name='initiate-payment'),
    path('callback/', PaymentCallbackView.as_view(), name='callback')
]
