from django.urls import path
from . import views

urlpatterns = [
    path('calculate_trade_pnl/', views.calculate_trade_pnl, name='calculate_trade_pnl'),
    path('save_trade/', views.save_trade, name='save_trade'),
]
