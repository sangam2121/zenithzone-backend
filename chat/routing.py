from django.urls import re_path
from . import consumers



websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<userId>[0-9a-f-]+)/(?P<otherUserId>[0-9a-f-]+)$', consumers.ChatConsumer.as_asgi()),
]
# ws://localhost:8000/ws/chat/297ccaf9-a5fb-45d8-b495-2174c644c051/db12fbf0-0c14-4d99-b1a9-0fa348feabcb