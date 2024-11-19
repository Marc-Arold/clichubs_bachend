from django.db import models
from offers.models import LaunchedOffer
from accounts.models import GamblerProfile

class FootballEvent(models.Model):   
    offer = models.ForeignKey(LaunchedOffer, on_delete=models.CASCADE)
    number_of_options_per_match = models.IntegerField()
    odds_min = models.FloatField()
    odds_max = models.FloatField()
    number_max_to_lose = models.IntegerField()
    percentage_loss_offer = models.FloatField()


class Match(models.Model):
    footballevent = models.ForeignKey(FootballEvent, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    start_time = models.TimeField()
    league_name = models.CharField(max_length=255)
    fixure_id_api = models.BigIntegerField()
    league_country = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.league_name} - {self.date}'

class Bookmaker(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='bookmakers')
    name = models.CharField(max_length=255, unique=True)
    bookmaker_id_api = models.BigIntegerField()

    def __str__(self):
        return self.name

class Bet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='bets')
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE)
    bet_name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    odd = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.bookmaker.name} - {self.bet_name} - {self.value} - {self.odd}'
    

class ChoiceGambler(models.Model):
    gambler = models.ForeignKey(GamblerProfile, on_delete=models.CASCADE)
    offer = models.ForeignKey(LaunchedOffer, on_delete=models.CASCADE)
    footballevent = models.ForeignKey(FootballEvent, on_delete=models.CASCADE)
    maximum_payout = models.FloatField()
    status_result = models.CharField(max_length=255)

class MatchGambler(models.Model): 
    choicegambler = models.ForeignKey(ChoiceGambler, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    start_time = models.TimeField()
    league_name = models.CharField(max_length=255)
    fixure_id_api = models.BigIntegerField()
    league_country = models.CharField(max_length=255)


class BetGambler(models.Model):
    match = models.ForeignKey(MatchGambler, on_delete=models.CASCADE, related_name='betsGambler')
    bet_name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    odd = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.bookmaker.name} - {self.bet_name} - {self.value} - {self.odd}'

