from django.shortcuts import render, redirect
from .models import WithdrawalCompanies
from .forms import WithdrawalFormCompanies
from balance_handler_companies.models import BalanceCompanies
from .config import MONCASH_CLIENT_ID, MONCASH_SECRET_KEY
import decimal
from django.contrib.auth.decorators import login_required
from django.db import transaction
import re
import requests
from django.http import JsonResponse

def phone_validator(phone_numer):
    phone_number_regex = r'^\d{8}$'
    match = re.search(phone_number_regex, phone_numer)
    if match:
        return True
    return False


def withdrawal(request):
    return render(request, 'withdrawals/withdrawals_companies.html')
    

def withdrawal_list(request):
    withdrawals = WithdrawalCompanies.objects.all()
    return render(request, 'withdrawals/withdrawal_list_companies.html', {'withdrawals': withdrawals})


def withdrawal_list_for_current_user(request):
    if request.user.is_authenticated:
        current_user_id = request.user.id
        withdrawals = WithdrawalCompanies.objects.filter(gambler=current_user_id)
        return render(request, 'withdrawals/withdrawal_list_for_user.html', {'withdrawals': withdrawals})
    else:
        # Handle the case when the user is not logged in
        return render(request, 'withdrawals/not_logged_in.html')
    


def get_moncash_access_token():
    url = "https://moncashbutton.digicelgroup.com/Api/oauth/token"
    headers = {"Accept": "application/json"}
    data = {"scope": "read,write", "grant_type": "client_credentials"}

    response = requests.post(url, auth=(MONCASH_CLIENT_ID, MONCASH_SECRET_KEY), headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to obtain Mon Cash access token.")

@login_required
@transaction.atomic
def withdraw_moncash(request):
    # Retrieve the amount to be withdrawn and the receiver account from the request data
    user = request.user


    amount = request.POST.get('amount_withdrawal')

    # validate the amount to withdraw entry 
    try:
            amount = decimal.Decimal(amount)
              # Convert to Decimal for financial calculations
            if amount <= 0:
                raise ValueError("Withdraw amount must be a positive number.")
    except decimal.InvalidOperation:
            return render(request, 'withdrawals/withdrawalerror_companies.html', {'error_message': 'Invalid withdraw amount.'})
    except ValueError as e:
            return render(request, 'withdrawals/withdrawalerror_companies.html', {'error_message': str(e)})

    #Validate phone number entry
    receiver = request.POST.get('receiver_account')
    if phone_validator(receiver)== False:
         return render(request, 'withdrawals/withdrawalerror_companies.html', {'error_message': 'Invalid withdraw phone number.'})
    

    # Moncash API base URL
    moncash_api_url = 'https:// moncashbutton.digicelgroup.com/Api/v1/Transfert'

    # Moncash API access token
    access_token = get_moncash_access_token()

    # Request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    # Request payload
    payload = {
        'amount': amount,
        'receiver': receiver,
        'desc': 'Withdrawal from MyApp',  # Customize the description as needed
    }

    try:
        # Make the API call to Moncash to initiate the withdrawal
        response = requests.post(moncash_api_url, headers=headers, json=payload)

        # Check the API response status code
        if response.status_code == 200:
            data = response.json()
            # Check if the API response contains the transaction details
            if 'transfer' in data and 'transaction_id' in data['transfer']:
                transaction_id = data['transfer']['transaction_id']
                # Save the withdrawal information in the database
                with transaction.atomic():
                     
                    WithdrawalCompanies.objects.create(
                        withdrawal_id=transaction_id,
                        company = user,
                        withdrawal_amount=amount,
                        withdrawal_phone_number=receiver,
                        withdrawal_method = 'Mon Cash',
                        withdrawal_status = 'Success',
                        withdrawal_date = data['timestamp']
                        # Add other relevant fields for the Withdraw model
                    )
                # Return a JSON response with the success message
                    balance = BalanceCompanies.objects.filter(company = user)
                    balance.balance_globale = balance.balance_globale - amount
                    balance.save()
                return JsonResponse({'message': 'Withdrawal successful'})

        # If the API response does not contain the expected data, return an error message
        return JsonResponse({'error_message': 'Withdrawal failed'}, status=400)

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the API call
        # For example, log the error or display an error message to the user
        return JsonResponse({'error_message': str(e)}, status=500)
