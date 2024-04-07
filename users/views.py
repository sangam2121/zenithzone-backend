from .serializers import RegisterSerializer, CustomUserSerializer
from rest_framework import generics
from django.shortcuts import render

from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser as User
from rest_framework.response import Response
from rest_framework import status


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.validated_data
        user = User.objects.create_user(
            email=user['email'],
            password=user['password'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            user_type=user['user_type'],
            phone=user['phone'],
            address=user['address'],
            bio=user['bio'],
        )

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data = {
                'message': 'User created successfully',
                'user': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'User could not be created: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # check the id from lookup field to be same to self id, if not redirect to own

        return self.request.user


    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Profile updated successfully',
                'user': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Profile could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class VerifyTokenView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)