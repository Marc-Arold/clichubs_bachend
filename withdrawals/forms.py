
from django import forms
from .models import Withdrawal

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['withdrawal_amount', 'withdrawal_phone_number', 'withdrawal_method']
