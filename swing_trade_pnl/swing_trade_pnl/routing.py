from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from trade import routing as trade_routing

# Define the routing configuration here
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            trade_routing.websocket_urlpatterns  # Include WebSocket routing from the trade app
        )
    ),
})
