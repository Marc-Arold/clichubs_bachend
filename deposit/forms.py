from django import forms
from .models import Deposit

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['deposit_amount', 'deposit_phone_number', 'deposit_method']
