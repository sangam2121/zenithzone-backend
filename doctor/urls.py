from django.urls import path
from rest_framework import routers
from . import views
from django.urls import include

# router for EducationViewSet

router = routers.DefaultRouter()
router.register(r'education', views.EducationViewSet)
router.register(r'experience', views.ExperienceViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('lists/', views.DoctorListAPIView.as_view()),
    path('clinics/', views.ClinicListCreateAPIView.as_view()),
    path('reviews/lists/', views.ReviewListAPIView.as_view()),
    path('reviews/create/', views.ReviewCreateAPIView.as_view()),
    path('review/<slug:pk>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view()),
    path('update/<slug:user__id>/', views.DoctorRetrieveUpdateAPIView.as_view()),
    path('delete/<slug:user__id>/', views.DoctorDestroyAPIView.as_view()),
    path('clinic/<slug:pk>/', views.ClinicRetrieveUpdateDestroyAPIView.as_view()),
]
