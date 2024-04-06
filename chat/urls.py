from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageListAPIView, ChatRoomListAPIView


urlpatterns = [
    path('chatrooms/', ChatRoomListAPIView.as_view(), name='chatrooms-list'),
    path('messages/', MessageListAPIView.as_view(), name='messages-list'),
]