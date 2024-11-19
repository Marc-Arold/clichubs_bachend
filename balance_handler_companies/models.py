from django.db import models
from companies_accounts.models import CompanyProfile
from django.utils import timezone
# Create your models here.

class BalanceCompanies(models.Model):
    balance_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, to_field='company_id')
    balance_globale = models.FloatField(null=True)
    balance_date = models.DateTimeField(default= timezone.now)