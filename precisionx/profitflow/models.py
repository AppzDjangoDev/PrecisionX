from django.db import models

class TradingOrder(models.Model):
        # Updated stock_name field with choices
    STOCK_CHOICES = [
        ('NIFTY', 'NIFTY'),
        ('BANKNIFTY', 'BANKNIFTY'),
    ]
    order_id = models.CharField(max_length=50, unique=True)
    stock_name = models.CharField(max_length=10, choices=STOCK_CHOICES, default=('BankNifty', 'BankNifty'))
    entry_time = models.DateTimeField(null=True, blank=True)
    entry_price = models.FloatField(null=True, blank=True)
    stop_loss = models.FloatField(default=5)
    strike_ltp = models.FloatField()
    buy_target = models.FloatField()
    option_type = models.CharField(max_length=4, choices=[('CE', 'CE'),('PE', 'PE')], default=('CALL', 'CALL'))
    strike_type = models.CharField(max_length=6, choices=[('ATM', 'ATM'), ('ITM', 'ITM'), ('OTM', 'OTM')], default=('STRIKE', 'Strike'))
    trailing_stop_loss_interval = models.IntegerField(default=5)
    trailing_stop_loss = models.FloatField(default=5)
    exit_time = models.DateTimeField(blank=True, null=True)
    exit_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.option_type} Option - {self.entry_time}"
    

from django.db import models
from django.utils import timezone

class AngelaApiLog(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    endpoint = models.CharField(max_length=255)
    request_data = models.JSONField()
    response_data = models.JSONField()
