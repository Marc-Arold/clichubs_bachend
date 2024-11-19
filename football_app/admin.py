from django.contrib import admin
from .models import FootballEvent, Match, Bookmaker, Bet,ChoiceGambler, MatchGambler, BetGambler
# Register your models here.


admin.site.register(FootballEvent)
admin.site.register(Match)
admin.site.register(Bookmaker)
admin.site.register(Bet)
admin.site.register(ChoiceGambler)
admin.site.register(MatchGambler)
admin.site.register(BetGambler)