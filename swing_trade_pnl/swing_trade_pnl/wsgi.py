import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swing_trade_pnl.settings')

application = get_wsgi_application()

print("WSGI application initialized")