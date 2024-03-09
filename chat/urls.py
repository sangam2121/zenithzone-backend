from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomCreateAPIView, MessageCreateAPIView, MessageListAPIView, ChatRoomListAPIView

router = DefaultRouter()
# router.register(r'(?P<chat_room_id>[0-9a-f-]+)/messages',
                # MessageViewSet, basename='messages')
# router.register(r'messages',
#                 MessageViewSet, basename='messages')

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('chatrooms/create', ChatRoomCreateAPIView.as_view(), name='chatrooms-create'),
    path('chatrooms/', ChatRoomListAPIView.as_view(), name='chatrooms-list'),
    path('messages/create', MessageCreateAPIView.as_view(), name='messages-create'),
    path('messages/', MessageListAPIView.as_view(), name='messages-list'),

]
