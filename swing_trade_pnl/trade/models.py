import uuid
from django.db import models
from django.conf import settings

class Trade(models.Model):
    tradeid = models.UUIDField(null=True)  # Make tradeid nullable initially
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scrip = models.CharField(max_length=100)
    trade_date = models.DateField()
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    margin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    exchange = models.CharField(max_length=50, null=True, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pnl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interest_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.scrip} - {self.trade_date} - {self.user.username}"
