from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from .models import Doctor, Review, Clinic
from django.db.models import Q
from .serializers import DoctorSerializer, ReviewSerializer, ClinicSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


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

    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         response = super().retrieve(request, *args, **kwargs)
    #         response.data = {
    #             'message': 'Doctor retrieved successfully',
    #             'doctor': response.data
    #         }
    #         return response
    #     except Exception as e:
    #         return Response({'error': 'Doctor could not be retrieved: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


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


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
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
        if instance.patient != self.request.user:
            raise PermissionError(
                'You are not allowed to update this review'
            )
    
    def perform_destroy(self, instance):
        if instance.patient != self.request.user:
            raise PermissionError(
                'You are not allowed to delete this review'
            )

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


class ClinicListCreateAPIView(generics.ListCreateAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Clinic.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__istartswith=name)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data = {
                'message': 'Clinic created successfully',
                'clinic': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Clinic could not be created: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class ClinicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Clinic updated successfully',
                'clinic': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Clinic could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            response.data = {
                'message': 'Clinic deleted successfully',
                'clinic': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Clinic could not be deleted: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
