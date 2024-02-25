from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
router.register(r'(?P<chat_room_id>[0-9a-f-]+)/messages',
                MessageViewSet, basename='messages')

urlpatterns = router.urls
