from rest_framework_simplejwt.views import TokenRefreshView
# authentication
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()


urlpatterns = [
    path('login/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('users/', views.UserListView.as_view(), name='users_list'),
    path('update/', views.UserUpdateView.as_view(), name='update_profile'),
    path('verify/', views.VerifyTokenView.as_view(), name='verify_token'),
    path('change/', views.ChangePasswordView.as_view(), name='change_password'),
    path('reset_token/', views.ResetPasswordTokenView.as_view(), name='reset_password_token'),
    path('reset/', views.ResetPasswordView.as_view(), name='reset_password'),

]
