"""
ASGI config for zenithzone project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""



from channels.layers import get_channel_layer
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zenithzone.settings')
django.setup()

import chat.routing

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
