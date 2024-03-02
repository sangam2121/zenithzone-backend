from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('lists/', views.PatientListView.as_view()),
    path('update/<slug:user__id>/', views.PatientUpdateView.as_view()),
    path('delete/<slug:user__id>/', views.PatientDeleteView.as_view()),
]
