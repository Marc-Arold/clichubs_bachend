# withdrawals/models.py

from django.db import models
from companies_accounts.models import CompanyProfile

class WithdrawalCompanies(models.Model):
    withdrawal_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, to_field='company_id')
    withdrawal_date = models.DateField()
    withdrawal_amount = models.FloatField()
    withdrawal_phone_number = models.CharField(max_length=255)
    withdrawal_method = models.CharField(max_length=255)
    withdrawal_status = models.CharField(max_length=255)

    def __str__(self):
        return f"Withdrawal ID: {self.withdrawal_id}, Company: {self.company}, Amount: {self.withdrawal_amount}"
