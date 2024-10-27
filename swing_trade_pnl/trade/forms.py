from django import forms

class TradeForm(forms.Form):
    scrip = forms.CharField(label='Scrip', max_length=10)
    buy_price = forms.FloatField(label='Buy Price')
    quantity = forms.IntegerField(label='Quantity')
    trade_date = forms.DateField(label='Trade Date', widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    margin = forms.FloatField(label='Margin (2x, 3x, etc.)')
    interest_rate = forms.FloatField(label='Daily Interest Rate (%)', initial=0.04)
    exchange = forms.ChoiceField(choices=[('NSE', 'NSE'), ('BSE', 'BSE')], label='Stock Exchange')  # New field for exchange
