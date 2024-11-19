
# Create your views here.
from django.shortcuts import render
from .models import Balance
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from accounts.models import GamblerProfile
from django.http import JsonResponse

# Create your views here.
@login_required
def balance_handler(request):
    return render(request, 'balance_handler/balance.html')

@login_required
def balance(request):
    current_user = request.user
    current_user_phone_number = current_user.phone_number
    gambler_profile = GamblerProfile.objects.get(phone_number=current_user_phone_number)
    
    balance_user = Balance.objects.filter(gambler=gambler_profile).order_by('-balance_date').first()
    balance_globale = balance_user.balance_globale
    balance_transfert = balance_user.balance_transfert
    balance_bonus = balance_user.balance_bonus
    balances = {"balance_globale":balance_globale, 
                "balance_transfert":balance_transfert,
                "balance_bonus":balance_bonus }
    #balances = JsonResponse(balances)
    print(balances)
    return render(request, 'balance_handler/balances.html', context=balances)

@login_required
def conversion_bonus(request):
    current_user = request.user
    current_user_phone_number = current_user.phone_number
    
    try:
        gambler_profile = GamblerProfile.objects.get(phone_number=current_user_phone_number)
    except GamblerProfile.DoesNotExist:
        return render(request, 'balance_handler/balance_bonus_conversion_error.html', {'error_message': 'Gambler profile not found.'})

    balance = Balance.objects.filter(gambler=gambler_profile).order_by('-balance_date').first()
    print(balance)
    if balance is not None:
        balance_bonus = balance.balance_bonus
        balance_user_before_conversion = balance.balance_globale
        CONVERSION_RATE = 0.10
        new_balance = (balance_bonus * CONVERSION_RATE) + balance_user_before_conversion
        balance.balance_globale = new_balance
        balance.balance_bonus = 0
        balance.save()
    else:
        return render(request, 'balance_handler/balance_bonus_conversion_error.html', {'error_message': 'Balance not found.'})

    return render(request, 'balance_handler/balances.html')

    
