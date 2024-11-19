from django.db import models
from offers.models import LaunchedOffer
from accounts.models import GamblerProfile
# Create your models here.

class HorseDescriptionGame(models.Model):
    offer = models.ForeignKey(LaunchedOffer, on_delete=models.CASCADE,)
    # Horse Names & Odds
    horse_name = models.JSONField()  # Store horse names and odds as JSON
    #price_min = models.FloatField()
    odd_min = models.FloatField()
    number_of_horses_allowed = models.IntegerField()
    bonus = models.FloatField()
    jackpot = models.FloatField()
    # amount_max_game = models.FloatField()

    def __str__(self):
        return f"Game Description for Offer {self.horse_name}"

class HorseGameUser(models.Model):
    gambler = models.ForeignKey(GamblerProfile, on_delete=models.CASCADE)
    description_horse_race = models.ForeignKey(HorseDescriptionGame, on_delete=models.CASCADE)
    odds_game = models.FloatField()
    horse_selected = models.JSONField()  # Store selected horse names as JSON
    maximum_payout = models.FloatField()
    status_result = models.CharField(max_length=255)

    def __str__(self):
        return f"Horse Game by User {self.gambler_id} for Race {self.description_horse_race_id}"
