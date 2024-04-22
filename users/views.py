from .serializers import RegisterSerializer, CustomUserSerializer
from rest_framework import generics
from django.shortcuts import render
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser as User, OTPstore
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import uuid
import jwt
import datetime

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
            bio=user.get('bio', None),
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


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            user = request.user
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            if not user.check_password(old_password):
                return Response({'error': 'Old password is incorrect', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordTokenView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            email = request.data.get('email')
            user = User.objects.get(email=email)
            token =  user.get_reset_password_token()
            send_mail(
                'Password Reset',
                f'Your password reset token is {token}.This token will expire after 10 minutes. Use this token to reset your password.\nIf you did not request a password reset, please ignore this email.\n***This is an automated email. Please do not reply.***',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            email = request.data.get('email')
            token = request.data.get('token')
            password = request.data.get('password')
            user = User.objects.get(email=email)
            expired = OTPstore.objects.filter(email=email , otp=token, created_at__gt=datetime.datetime.now()-datetime.timedelta(minutes=5)).exists()
            if not expired:
                return Response({'error': 'Invalid token or expired token.', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                OTPstore.objects.filter(email=email, otp=token).delete()
            token = str(token)
            token, xord = token[:4], token[4:8]
            decoded = int(xord)^int(str(int(user.id))[-4:])
            if (decoded!=int(token)):
                return Response({'error': 'Invalid token', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}', 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)