import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swing_trade_pnl.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from trade import routing  # Update this line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swing_trade_pnl.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
print("ASGI application initialized")