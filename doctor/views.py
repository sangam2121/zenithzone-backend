from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from .models import Doctor, Review, Education, Experience
from django.db.models import Q
from .serializers import DoctorSerializer, ReviewSerializer, EducationSerializer, ExperienceSerializer,  ReviewListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


class DoctorListAPIView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Doctor.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(Q(user__first_name__istartswith=name) | Q(user__last_name__istartswith=name))
        speciality = self.request.query_params.get('speciality', None)
        if speciality is not None:
            queryset = queryset.filter(speciality__istartswith=speciality)
        clinic_name = self.request.query_params.get('clinic_name', None)
        if clinic_name is not None:
            queryset = queryset.filter(clinic__name__istartswith=clinic_name)
        return queryset


class DoctorRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'user__id'


    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            
            response.data = {
                'message': 'Doctor updated successfully',
                'doctor': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Doctor could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class DoctorDestroyAPIView(generics.DestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'user__id'


class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.all()
        doctor = self.request.query_params.get('doctor', None)
        keyword = self.request.query_params.get('keyword', None)
        if keyword is not None:
            queryset = queryset.filter(content__icontains=keyword)
        if doctor is not None:
            queryset = queryset.filter(doctor__id=doctor)
        return queryset

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data = {
                'message': 'Review created successfully',
                'review': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Review could not be created: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.patient.user != self.request.user:
            raise PermissionError(
                'You are not allowed to update this review'
            )
        
        
    
    def perform_destroy(self, instance):
        if instance.patient.user != self.request.user:
            print(instance.patient, self.request.user)
            raise PermissionError(
                'You are not allowed to delete this review'
            )
        instance.delete()

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Review updated successfully',
                'review': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Review could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            response.data = {
                'message': 'Review deleted successfully',
                'review': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Review could not be deleted: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)



class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data = {
                'message': 'Education created successfully',
                'education': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Education could not be created: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Education updated successfully',
                'education': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Education could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


    

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data = {
                'message': 'Experience created successfully',
                'experience': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Experience could not be created: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Experience updated successfully',
                'experience': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Experience could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
