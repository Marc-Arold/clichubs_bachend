# withdrawals/models.py

from django.db import models
from accounts.models import GamblerProfile

class Withdrawal(models.Model):
    withdrawal_id = models.AutoField(primary_key=True)
    gambler = models.ForeignKey(GamblerProfile, on_delete=models.CASCADE, to_field='profile_id')
    withdrawal_date = models.DateField()
    withdrawal_amount = models.FloatField()
    withdrawal_phone_number = models.CharField(max_length=255)
    withdrawal_method = models.CharField(max_length=255)
    withdrawal_status = models.CharField(max_length=255)

    def __str__(self):
        return f"Withdrawal ID: {self.withdrawal_id}, Gambler: {self.gambler}, Amount: {self.withdrawal_amount}"
