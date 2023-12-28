from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('lists/', views.PatientListView.as_view()),
    path('update/<slug:pk>/', views.PatientUpdateView.as_view()),
    path('delete/<slug:pk>/', views.PatientDeleteView.as_view()),
]
