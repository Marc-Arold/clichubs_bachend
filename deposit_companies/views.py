import requests
from django.shortcuts import render, redirect, HttpResponse
from .models import DepositCompanies
#from .forms import DepositForm
from moncashify import API
import uuid
from django.http import JsonResponse
from balance_handler_companies.models import BalanceCompanies
import decimal
from django.db import transaction
from django.contrib.auth.decorators import login_required

# Import the configuration file
from .config import MONCASH_CLIENT_ID, MONCASH_SECRET_KEY


def deposit(request):
    return render(request, "deposit/deposit_companies.html")

@login_required
def deposit_list_for_current_user(request):
    if request.user.is_authenticated:
        current_user_id = request.user.id
        deposits_companies = DepositCompanies.objects.filter(company = current_user_id)
        return render(request, 'deposit/deposit_list_for_user_companies.html', {'deposits': deposits_companies})
    else:
        return render(request, 'deposit/not_logged_in_companies.html')


def generate_unique_order_id():
    # Generate a random UUID (Universally Unique Identifier)
    # The UUID will be a string in the format xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    unique_id = str(uuid.uuid4())

    # Remove the hyphens to get a clean alphanumeric string
    # For example, "5b54f03c-e6b0-4c2f-94b2-77bb5bf0a44e" becomes "5b54f03ce6b04c2f94b277bb5bf0a44e"
    clean_id = unique_id.replace('-', '')

    # Return the unique orderId
    return clean_id


def get_moncash_access_token():
    url = "https://moncashbutton.digicelgroup.com/Api/oauth/token"
    headers = {"Accept": "application/json"}
    data = {"scope": "read,write", "grant_type": "client_credentials"}

    response = requests.post(url, auth=(MONCASH_CLIENT_ID, MONCASH_SECRET_KEY), headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to obtain Mon Cash access token.")

#@login_required #pou w ajoute le app la fini pou konekte 
def deposit_moncash(request):
    if request.method == 'POST':
        amount_deposit = request.POST.get('amount_deposit')
        try:
            amount = decimal.Decimal(amount_deposit)
              # Convert to Decimal for financial calculations
            print(amount_deposit)
            if amount <= 0:
                raise ValueError("Deposit amount must be a positive number.")
        except decimal.InvalidOperation:
            return render(request, 'deposit/payment_error_companies.html', {'error_message': 'Invalid deposit amount.'})
        except ValueError as e:
            return render(request, 'deposit/payment_error_companies.html', {'error_message': str(e)})

        # Generate a unique orderId
        order_id = generate_unique_order_id()
      
        # Get Mon Cash access token
        access_token = get_moncash_access_token()

        # Create the payment instance connection with Mon Cash
        #moncash = API(MONCASH_CLIENT_ID, MONCASH_SECRET_KEY, False)

        try:
            # Process the payment
            amount = float(amount_deposit)

            # Prepare the payload for the API request
            payload = {
                "amount": amount,
                "orderId": order_id
            }

            # Set headers with the access token
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Make API request to create payment
            response = requests.post("https://moncashbutton.digicelgroup.com/Api/v1/CreatePayment", headers=headers, json=payload)
            if response.status_code == 202:
                # Payment request accepted, retrieve the redirect URL
                base_url = 'https://moncashbutton.digicelgroup.com/Moncash-middleware'
                to_add = '/Payment/Redirect?token='
                token = response.json()["payment_token"]["token"]
                url = base_url + to_add + token
    
                # Redirect the client to the Moncash terminal
                return redirect(url)
            else:
                # Handle errors if the payment request was not accepted
                error_message = response.json().get("error_message", "Payment request failed.")
                return render(request, 'deposit/payment_error_companies.html', {'error_message': error_message})

        except Exception as e:
            # Handle any errors that may occur during the payment process
            # For example, log the error or display an error message to the user
            return render(request, 'deposit/payment_error_companies.html', {'error_message': str(e)})

    else:
        return render(request, 'deposit/invalid_request_companies.html')
    
@login_required
@transaction.atomic
def deposit_callback(request):
    if request.method == 'POST':
        try:
            # Get the currently logged-in user
            user = request.user

            # Parse the POST data to get the transactionId and orderId
            data = request.POST
            transaction_id = data.get('transactionId')
            order_id = data.get('orderId')

            # Get Mon Cash access token
            access_token = get_moncash_access_token()

            # Create the payment instance connection with Mon Cash
            #moncash = API(MONCASH_CLIENT_ID, MONCASH_SECRET_KEY, True)

            # Prepare the payload for the API request
            payload = {
                "transactionId": transaction_id,
            }

            # Set headers with the access token
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Make API request to retrieve payment details
            response = requests.post("https://moncashbutton.digicelgroup.com/Api/v1/RetrieveTransactionPayment", headers=headers, json=payload)

            if response.status_code == 200:
                # Retrieve the payment details from the API response
                payment_details = response.json()["payment"]

                # Save the deposit information in the database, linking it to the user
            with transaction.atomic():
                deposit = DepositCompanies.objects.create(
                    deposit_id=order_id,
                    deposit_amount =payment_details.get('cost'),
                    company=user,
                    deposit_date=payment_details.get('timestamp'),
                    deposit_phone_number=payment_details.get('payer'),
                    deposit_method="Mon Cash",
                    deposit_status="Success"
                )

                # Update the user's balance
                balance = BalanceCompanies.objects.filter(company=user).first()
                if balance:
                    balance.balance_globale += payment_details.get('cost')
                    balance.save()
                else:
                    # Create a new balance entry if it doesn't exist
                    balance = BalanceCompanies.objects.create(company=user, balance_globale=payment_details.get('cost'))

            # Return a JSON response with the payment details
            return JsonResponse(payment_details)
        except Exception as e:
            # Handle any errors that may occur during the payment process
            # For example, log the error or display an error message to the user
            return JsonResponse({'error_message': str(e)}, status=500)

    else:
        return JsonResponse({'error_message': 'Invalid request method'}, status=400)
