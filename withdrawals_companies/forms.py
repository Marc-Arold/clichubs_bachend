
from django import forms
from .models import WithdrawalCompanies

class WithdrawalFormCompanies(forms.ModelForm):
    class Meta:
        model = WithdrawalCompanies
        fields = ['withdrawal_amount', 'withdrawal_phone_number', 'withdrawal_method']
