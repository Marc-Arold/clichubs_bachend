from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import datetime, timedelta
from .config import X_RapidAPI_Key
from balance_handler_companies.models import BalanceCompanies
from balance_handler.models import Balance
from companies_accounts.models import CompanyProfile
from offers.models import LaunchedOffer
from .models import FootballEvent, Match, Bet, Bookmaker, MatchGambler, BetGambler, ChoiceGambler
from django.core.exceptions import ObjectDoesNotExist
import json
# Create your views here.
def countries():
    url = 'https://football-pro.p.rapidapi.com/api/v2.0/countries'
    headers = {'x-rapidapi-host': 'football-pro.p.rapidapi.com', 'x-rapidapi-key': X_RapidAPI_Key}
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    countries_dict = {
        "contries_infos": [{"code":country["code"],"name": country["name"], "flag": country["flag"]} for country in data["response"]]
    }
    return JsonResponse(countries_dict)

def get_countries(request):
    response = countries()
    print(response)
    return response

def leagues():
    url = 'https://football-pro.p.rapidapi.com/api/v2.0/leagues'
    headers = {'x-rapidapi-host': 'football-pro.p.rapidapi.com', 'x-rapidapi-key': X_RapidAPI_Key}
    response = requests.get(url, headers=headers).json()
    leagues_dict = {
         "leagues_infos": [{"id": league["id"],"name": league["name"], "logo":league["logo_path"], "country_id": league['country_id'] }
                            for league in response["data"]]
    }
    return JsonResponse(leagues_dict)

def get_leagues(request):
    response = leagues()
    return response

def bookmakers():
    url = 'https://football-pro.p.rapidapi.com/api/v2.0/bookmakers'
    headers = {'x-rapidapi-host': 'football-pro.p.rapidapi.com', 'x-rapidapi-key': X_RapidAPI_Key}
    response = requests.get(url, headers=headers).json()
    bookmakers_dict = {
         "bookmarkers_infos": [{"id": bookmaker["id"], "name": bookmaker["name"]}
                            for bookmaker in response["data"]]
    }
    return JsonResponse(bookmakers_dict)

def get_bookmakers(request):
    response = bookmakers()
    return response

def fixures_for_a_week():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    url = f'https://football-pro.p.rapidapi.com/api/v2.0/fixtures/between/{start_date_str}/{end_date_str}'
    headers = {'x-rapidapi-host': 'vfootball-pro.p.rapidapi.com', 'x-rapidapi-key': X_RapidAPI_Key}
    response = requests.get(url, headers=headers).json()
    fixures_dict = {
         "fixures_infos": [{"id_fixures": fixure["id"], 
                            "team_1_name": fixure["localTeam"]["data"]["name"],
                            "team_1_logo": fixure["localTeam"]["data"]["logo_path"],
                            "team_2_name": fixure["visitorTeam"]["data"]["name"],
                            "team_2_logo": fixure["visitorTeam"]["data"]["logo_path"],}
                                for fixure in response["data"]]
    }
    return JsonResponse(fixures_dict)

def get_fixures_for_a_week(request):
    response = fixures_for_a_week()
    return response


def odds_for_fixtures_in_week():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    url = f'https://football-pro.p.rapidapi.com/api/v2.0/fixtures/between/{start_date_str}/{end_date_str}'
    headers = {'x-rapidapi-host': 'football-pro.p.rapidapi.com', 'x-rapidapi-key': X_RapidAPI_Key}
    response = requests.get(url, headers=headers).json()
    fixtures_odds_dict = {
        "fixtures_odds_infos": [
            {
                "id_fixture": fixture["id"],
                "league_id": fixture["league_id"],
                "team_1_name": fixture["localteam_id"],
                "team_2_name": fixture["visitorteam_id"],
                "odds": [
                    {
                        "label": odd["label"],
                        "value": odd["value"],
                        "probability": odd["probability"]
                    }
                    for bookmaker in fixture["flatOdds"]["data"]
                    for odd in bookmaker["odds"]
                ]
            }
            for fixture in response["data"]
        ]
    }
    return JsonResponse(fixtures_odds_dict)

def get_odds_for_fixtures_in_week(request):
    response = odds_for_fixtures_in_week()
    return response


def create_football_event(request):
    try:
        # Retrieve the input of the user
        user = request.user
        matches_chosen = request.POST.getlist('matches')
        odds_of_matches = request.POST.getlist('odds')
        odds_min = float(request.POST.get('odds_min'))
        odds_max = float(request.POST.get('odds_max'))
        price_offer_min = float(request.POST.get('price_offer_min'))
        percentage_of_money_after_loss = float(request.POST.get('percentage'))
        gain_offer_max = request.POST.get('gain_offer_max')

        if not all([matches_chosen, odds_of_matches, odds_min, odds_max, percentage_of_money_after_loss, chosen_bookmaker,gain_offer_max]):
            return JsonResponse({'error': 'Invalid input'})
        
        company = CompanyProfile.objects.get(company_id = user.id)
            #

            # Check balance
        balance = BalanceCompanies.objects.filter(company=user).order_by('-balance_date').first()
        if balance < gain_offer_max:
            return JsonResponse({"error": "Insufficient funds to launch game"}, status=400)
        
        theoffer = LaunchedOffer.objects.create(
                company=company,
                price_offer_min = price_offer_min,
                gain_offer_max = gain_offer_max,
                offer_type = 'FOOT BALL',
                offer_launched_status = 'Launched'
            )
        theoffer.save()
        football_event = FootballEvent.objects.create(
         
            offer=theoffer,
            number_of_options_per_match=len(matches_chosen),
            odds_min=odds_min,
            odds_max=odds_max,
            percentage_loss_offer=percentage_of_money_after_loss
        )
        football_event.save()

        # Iterate through the matches chosen
        for match_data in matches_chosen:
            # Extract match details
            match_name = match_data["mach_name"]
            date = match_data["date"]
            date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            time_obj = date_obj.time()
            league_name = match_data["league_name"]
            fixure_id = match_data["fixure_id"]
            league_country = match_data["league_country"]  # Extract if available
            chosen_bookmaker = match_data["bookmaker"]
            bets = match_data["bets"]

            # Create the Match object
            match = Match.objects.create(
                match_name=match_name,
                date=date,
                start_time=time_obj , 
                fixure_id_api = fixure_id,
                league_name=league_name,
                league_country=league_country if league_country else league_name
            )
            
            # Get or create the Bookmaker object
            bookmaker, _ = Bookmaker.objects.get_or_create(name=chosen_bookmaker,match = match)

            # Create Bet objects for the match
            for bet_data in bets:
                bet_name = bet_data["name"]
                for value_data in bet_data["values"]:
                    value = value_data["value"]
                    odd = value_data["odd"]
                    Bet.objects.create(
                        match=match,
                        bookmaker=bookmaker,
                        bet_name=bet_name,
                        value=value,
                        odd=odd
                    )
        
        if balance:
            balance.balance_globale -= gain_offer_max
            balance.save()
            return JsonResponse({"message": "Football Event created successfully"})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid data format"}, status=400)
    


def create_selection(request,foot_ball_event_id):
    try:
        data= request.POST
        user = request.user
        maximum_payout = data.get('maximum_payout')
        odds_game = data.get('odds_game')
        matches = data.getlist("matches")
        
        foot_ball_event = FootballEvent.objects.get(id=foot_ball_event_id)
        offer = foot_ball_event.offer
        gain_offer_max = offer.gain_offer_max

        if gain_offer_max< maximum_payout:
            return JsonResponse({"error": "The company can't pay the maximum payout"}, status=400)
        
        for match in matches:
            if len(match["bets"])> foot_ball_event.number_of_options_per_match:
                return JsonResponse({"error": f"You have selected too more than {foot_ball_event.number_of_options_per_match} in the match {match['name']} "}, status=400)


        choice_gambler = ChoiceGambler.objects.create(
            gambler = user,
            offer = offer,
            footballevent = foot_ball_event,
            maximum_payout= maximum_payout,
            status_result = 'Pending'

        )
        
        for match_data in matches:
            # Extract match details
            match_name = match_data["mach_name"]
            date = match_data["date"]
            date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            time_obj = date_obj.time()
            league_name = match_data["league_name"]
            fixure_id = match_data["fixure_id"]
            league_country = match_data["league_country"] 
            bets = match_data["bets"]
            Bookmaker_name = match_data["Bookmaker_name"]
            bookmakers_id = Bookmaker.objects.filter(name = Bookmaker_name).first().bookmaker_id_api
            # Create the Match object
            match = MatchGambler.objects.create(
                match_name=match_name,
                date=date,
                start_time=time_obj , 
                fixure_id_api = fixure_id,
                league_name=league_name,
                league_country=league_country if league_country else league_name
            )
            
            # Get or create the Bookmaker object
          
            user_fixtures_bets = {}
            # Create Bet objects for the match
            for bet_data in bets:
                bet_name = bet_data["name"]
                for value_data in bet_data["values"]:
                    value = value_data["value"]
                    odd = value_data["odd"]
                    BetGambler.objects.create(
                        match=match,

                        bet_name=bet_name,
                        value=value,
                        odd=odd
                    )
                    
                fixture_key = match_data["fixure_id"]
                user_fixtures_bets[fixture_key] = {
                        "odd_name": bet_name,
                        "book_maker_id": bookmakers_id 
                    }
         #build a dictionnary (user_fixtures_bets) with every match choose by the user with the following keys: fixure_id, the name of the odd, the book_maker_id
          
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid data format","data_return": user_fixtures_bets}, status=400)

def process_selection(selection_id):
    try:
        choice_gambler = ChoiceGambler.objects.get(id=selection_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Selection not found"}, status=404)

    # Call the function to check user bets (assuming you have this function defined)
    results = check_user_bets(choice_gambler.user_fixtures_bets)

    number_of_losses = sum(1 for result in results if result == 'loss')

    foot_ball_event = choice_gambler.footballevent
    number_max_to_lose = foot_ball_event.number_max_to_lose
    percentage_loss_offer = foot_ball_event.percentage_loss_offer
    gain_offer_max = foot_ball_event.offer.gain_offer_max
    maximum_payout = choice_gambler.maximum_payout
    odds_game = choice_gambler.odds_game
    offer_choose_gambler = choice_gambler.offer
    company = offer_choose_gambler.company
    company_balance = BalanceCompanies.objects.filter(company=company).order_by('-balance_date').first()
    gambler = choice_gambler.gambler
    user_balance = Balance.objects.filter(gambler=gambler).order_by('-balance_date').first()
    final_decision = ''
    if number_of_losses>0 and number_of_losses<=number_max_to_lose:
        reimborse_amount = percentage_loss_offer*gain_offer_max
        user_balance.balance_globale += reimborse_amount
        final_decision = 'LOSE WITH REIMBORSEMENT'
    elif number_of_losses == 0:
        user_balance.balance_globale += gain_offer_max
        final_decision= 'WIN'
    else:
        bet_amount = maximum_payout / odds_game
        company_balance.balance_globale += bet_amount
        final_decision = 'LOSE'
    user_balance.save()
    company_balance.save()

    choice_gambler = ChoiceGambler.objects.create(
            gambler = gambler,
            offer = offer_choose_gambler,
            status_result = final_decision

        )
    choice_gambler.save() 

def check_user_bets(user_fixtures_bets):
    results = []
    for user_bet in user_fixtures_bets:
        fixture_id = user_bet['fixture_id']
        chosen_odds_label = user_bet['chosen_odds_label']
        bookmaker_id = user_bet['bookmaker_id']
        
        # Default result
        result = 'not found'

        # Fetch the actual fixture details
        url = f'https://football-pro.p.rapidapi.com/api/v2.0/fixtures/{fixture_id}'
        headers = {'x-rapidapi-host': 'football-pro.p.rapidapi.com', 'x-rapidapi-key': X_RapidAPI_Key}
        response = requests.get(url, headers=headers).json()
        fixture = response['data']

        # Find the winning odds label based on the bookmaker and label
        for bet in fixture["flatOdds"]["data"]:
            if bet["bookmaker_id"] == bookmaker_id and bet["suspended"] == 'false':
                for odd in bet["odds"]:
                    if odd["label"] == chosen_odds_label:
                        result = 'won' if odd["winning"] == 'true' else 'lost'
                        break

        results.append({
            'fixture_id': fixture_id,
            'chosen_odds_label': chosen_odds_label,
            'result': result
        })

    return JsonResponse({"user_bets_results": results})

def get_fooball_page(request):
    return render(request, 'football_app/football.html')