from django.db import models
from accounts.models import GamblerProfile
from django.utils import timezone
# Create your models here.

class Balance(models.Model):
    balance_id = models.AutoField(primary_key=True)
    gambler = models.ForeignKey(GamblerProfile, on_delete=models.CASCADE, to_field='profile_id')
    balance_globale = models.FloatField(null=True)
    balance_transfert = models.FloatField(null=True)
    balance_bonus = models.FloatField(null=True)
    balance_date = models.DateTimeField(default= timezone.now)