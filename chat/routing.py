from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r'ws/chat/(?P<userId>\w+)/(?P<otherUserId>\w+)/$',
        consumers.ChatConsumer.as_asgi()
    ),
]