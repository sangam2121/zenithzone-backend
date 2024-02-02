from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomView, MessageView

# router = DefaultRouter()
# router.register(r'messages', MessageViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('rooms', ChatRoomView.as_view()),
    path('messages/<uuid:chatroom_id>', MessageView.as_view(), name='messages'),
    path('users/<uuid:user_id>/chats', ChatRoomView.as_view(), name='chats'),
]
