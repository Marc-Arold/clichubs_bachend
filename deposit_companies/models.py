from django.db import models
from accounts.models import GamblerProfile
from companies_accounts.models import CompanyProfile

class DepositCompanies(models.Model):
    deposit_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, to_field='company_id')
    deposit_date = models.DateField()
    deposit_phone_number = models.CharField(max_length=255)
    deposit_method = models.CharField(max_length=255)
    deposit_amount = models.FloatField()
    deposit_status = models.CharField(max_length=255)

    def __str__(self):
        return f"Deposit ID: {self.deposit_id}, Amount: {self.deposit_amount}"