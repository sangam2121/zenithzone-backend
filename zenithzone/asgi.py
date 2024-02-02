"""
ASGI config for zenithzone project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.layers import get_channel_layer
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zenithzone.settings')

django_asgi_app = get_asgi_application()
channel_layer = get_channel_layer()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ),
    }
)
