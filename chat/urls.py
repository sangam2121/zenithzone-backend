from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomCreateListAPIView, MessageCreateListAPIView

router = DefaultRouter()
# router.register(r'(?P<chat_room_id>[0-9a-f-]+)/messages',
                # MessageViewSet, basename='messages')
# router.register(r'messages',
#                 MessageViewSet, basename='messages')

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('chatrooms/', ChatRoomCreateListAPIView.as_view(), name='chatrooms-list-create'),
    path('messages/', MessageCreateListAPIView.as_view(), name='messages-list-create'),

]
