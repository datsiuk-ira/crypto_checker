import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import market_analysis.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_analysis.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Define WebSocket URL routing
    "websocket": AuthMiddlewareStack(
        URLRouter(
            market_analysis.routing.websocket_urlpatterns
        )
    ),
})
