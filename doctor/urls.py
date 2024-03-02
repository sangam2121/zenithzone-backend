from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('lists/', views.DoctorListAPIView.as_view()),
    path('clinics/', views.ClinicListCreateAPIView.as_view()),
    path('reviews/', views.ReviewListCreateAPIView.as_view()),
    path('review/<slug:pk>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view()),
    path('update/<slug:user__id>/', views.DoctorRetrieveUpdateAPIView.as_view()),
    path('delete/<slug:user__id>/', views.DoctorDestroyAPIView.as_view()),
    path('clinic/<slug:pk>/', views.ClinicRetrieveUpdateDestroyAPIView.as_view()),
]
