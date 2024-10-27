from django.urls import re_path
from django.urls import path
from trade import consumers

websocket_urlpatterns = [
    re_path(r'^ws/pnl_updates/(?P<trade_id>[a-f0-9\-]+)/$', consumers.PnlConsumer.as_asgi()),
]
