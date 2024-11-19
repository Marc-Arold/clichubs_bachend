from django.shortcuts import render
from django.http import JsonResponse
from .models import HorseDescriptionGame,HorseGameUser
from offers.models import LaunchedOffer
from balance_handler_companies.models import BalanceCompanies
from companies_accounts.models import CompanyProfile
from balance_handler.models import Balance
from random import random
import requests
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@login_required
def create_horse_race(request):
    try:
        data = request.POST
        user = request.user
        float_fields = ['price_offer_min', 'gain_offer_max', 'bonus', 'jackpot']
        int_fields = ['number_of_horses_allowed']
        str_fields = ['horse_name']

        # Iterate over each group and perform the appropriate validation
        for field in float_fields + int_fields + str_fields:
            value = data.get(field)

            if not value:
                return JsonResponse({"error": f"{field} is missing"}, status=400)

            if field in float_fields and not isinstance(value, float):
                return JsonResponse({"error": f"{field} should be a float"}, status=400)

            if field in int_fields and not isinstance(value, int):
                return JsonResponse({"error": f"{field} should be an integer"}, status=400)

            if field in str_fields and not isinstance(value, str):
                return JsonResponse({"error": f"{field} should be a string"}, status=400)
        
        bonus=data.get('bonus')
        jackpot=data.get('jackpot')
        company = CompanyProfile.objects.get(company_id = user.id)
        # Check authorization

        # Check balance
        balance = BalanceCompanies.objects.filter(company=user).order_by('-balance_date').first()
        if balance < data['gain_offer_max'] + bonus + jackpot:
            return JsonResponse({"error": "Insufficient funds to launch game"}, status=400)

        #create the offer 
        theoffer = LaunchedOffer.objects.create(
            company=company,
            price_offer_min = data.get('price_offer_min'),
            gain_offer_max = data.get('gain_offer_max'),
            offer_type = 'HORSE RACE',
            offer_launched_status = 'Launched'
        )
        theoffer.save()
        # Create horse race
        horse_race = HorseDescriptionGame.objects.create(
            offer=theoffer,
            bonus=bonus,
            jackpot=jackpot,
            number_of_horses_allowed=data.get('number_of_horses_allowed'),
            horse_name=data.get('horse_name')  # assign the horse_name data here
        )
        horse_race.save()
        if balance:
                    balance.balance_globale -= data.get('gain_offer_max')
                    balance.balance_globale -= bonus
                    balance.balance_globale -= jackpot
                    balance.save()
        return JsonResponse({"message": "Horse race created successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid data format"}, status=400)
    
@login_required
def create_selection(request, game_description_id):
    try:
        data= request.POST
        user = request.user
        odds_game = data.get('odds_game')
        maximum_payout = data.get('maximum_payout')
        #retrieve the inputsfor the horses selected 
        #validate the inputs


        game_description = HorseDescriptionGame.objects.get(id=game_description_id)

        # Verify if the number of horses selected is less or equal than what the game description has fixed
        if len(data.get('horses_selected')) > game_description.number_of_horses_allowed:
            return JsonResponse({"error": "Too many horses selected"}, status=400)
        
        # Verify if the company can pay the user
        offer = game_description.offer
        gain_offer_max = offer.gain_offer_max
        if gain_offer_max< maximum_payout:
            return JsonResponse({"error": "The company can't pay the maximum payout"}, status=400)

        # Create a random function to know if we will give the bonus
        give_bonus = random.choice([True, False])

        # Create a random function to know if we will give the jackpot
        give_jackpot = random.choice([True, False])

        # Fire the horse race game
        response = requests.get('https://www.clichubs.com/horserace/firing')

        # Check if the request was successful
        if response.status_code != 200:
            return JsonResponse({"error": "Unable to fire the horse race game"}, status=500)

        # Retrieve the result of the game
        game_result = response.json().get('result')

        # Get the company balance
        company = offer.company
        company_balance = BalanceCompanies.objects.filter(company=company).first()

        # Get the user balance
        user_balance = Balance.objects.filter(gambler=user).first()

        # If the user wins the game, add the maximum payout to his balance, and possibly bonus and jackpot
        if game_result == 'win':
            user_balance.balance_globale += maximum_payout
        
            if give_bonus:
                user_balance.balance_globale += game_description.bonus
    
            if give_jackpot:
                user_balance.balance_globale += game_description.jackpot
                #company_balance.balance_globale -= game_description.jackpot
        else:  # The user loses the game
            bet_amount = maximum_payout / odds_game
            company_balance.balance_globale += bet_amount + game_description.bonus + game_description.jackpot

        user_balance.save()
        company_balance.save()

        # Register the information in the HorseGameUser table
        HorseGameUser.objects.create(
            user=user,
            game_description=game_description,
            odds_game=odds_game,
            maximum_payout=maximum_payout,
            horses_selected=data.get('horses_selected'),
            result=game_result,
            bonus_given=give_bonus,
            jackpot_given=give_jackpot
        )

        return JsonResponse({"message": "Selection created successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid data format"}, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_horse_races_by_company(request, company_id):
    try:
        # Get the company
        company = CompanyProfile.objects.get(company_id=company_id)
        #get the offers 
        offers = LaunchedOffer.objects.filter(company_id = company_id, offer_launched_status='Launched')
        
        # Get all horse race games by this company where the offer is launched
        horse_races = HorseDescriptionGame.objects.filter(offer = offers)
        
        horse_race_list = []
        for horse_race in horse_races:
            horse_race_dict = {
                'company_name': company.company_name,
                'company_slogan': company.company_slogan,
                'price_offer_min': horse_race.offer.price_offer_min,
                'odd_min': horse_race.odd_min,
                'number_of_horses_allowed': horse_race.number_of_horses_allowed,
                'bonus': horse_race.bonus,
                'jackpot': horse_race.jackpot,
                'horses': horse_race.horse_name,
            }
            horse_race_list.append(horse_race_dict)
            
        return JsonResponse(horse_race_list, safe=False)
    except CompanyProfile.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)