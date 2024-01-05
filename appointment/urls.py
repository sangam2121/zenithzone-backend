from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='create'),
    path('lists/', AppointmentListView.as_view(), name='list'),
    path('update/<slug:id>/', AppointmentUpdateView.as_view(), name='update'),

]
