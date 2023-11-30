# forms.py
from django import forms
from .models import TradingOrder

class TradingOrderForm(forms.ModelForm):
    class Meta:
        model = TradingOrder
        exclude = ['entry_time', 'entry_price', 'exit_time', 'exit_price', 'order_id', 'strike_ltp']
        widgets = {
            'option_type': forms.Select(attrs={'class': 'form-control'}),
            'strike_type': forms.Select(attrs={'class': 'form-control'}),
            'buy_target': forms.NumberInput(attrs={'class': 'form-control'}),
            'stop_loss': forms.NumberInput(attrs={'class': 'form-control'}),
            'trailing_stop_loss_interval': forms.NumberInput(attrs={'class': 'form-control'}),
            'trailing_stop_loss': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_name': forms.Select(attrs={'class': 'form-control'}),
        }
