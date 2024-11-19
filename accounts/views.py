from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import GamblerUserCreationForm
from django.contrib import messages
from .models import PasswordChange,GamblerProfile, GamblerUser
from datetime import datetime
import secrets
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import nexmo
from twilio.rest import Client
from django_ratelimit.decorators import ratelimit
from .config import NEXMO_API_KEY, NEXMO_API_SECRET, NEXMO_PHONE_NUMBER, ACCOUNT_SID,AUTH_TOKEN,Twillio_PHONE


def register_user(request):
    form = GamblerUserCreationForm(request.POST)
    if request.method == 'POST':
        form = GamblerUserCreationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone_number = form.cleaned_data.get('phone_number')
            sex = form.cleaned_data.get('sex')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            password = form.cleaned_data.get('password1')
            print(form)
            # Create a new GamblerProfile instance
            profile = GamblerProfile(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                sex=sex,
                date_of_birth=date_of_birth,
            )
            profile.save()

            # Create a new GamblerUser instance
            #user_model = get_user_model()
            user = GamblerUser.objects.create_user(
                phone_number=phone_number,
                password=password,
                first_name=first_name,
                last_name=last_name,
                sex=sex,
                date_of_birth=date_of_birth,
                profile=profile,  # Assign the created profile to the user's profile field
            )
            user.save()

            return redirect("accounts:login")
    else:
        form = GamblerUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
    
    
@ratelimit(key='ip', rate='100/d', block=True)
def user_login(request):
    if 'company' in request.session:
        request.session.clear()
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password1')
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            request.session['role'] = 'gambler'
            return redirect("accounts:register")
        else:
            messages.error(request, 'Ou mal antre nimewo telefòn oubyen Modpass la.')
            print('error')
    return render(request, 'accounts/login.html')


@ratelimit(key='ip', rate='10/d', block=True)
def password_recovery(request):
    if request.method == 'POST':
        phone_number = request.user.phone_number
        phone_recevery_by_user = request.POST.get('phone_number')

        if phone_number!= phone_recevery_by_user:
            messages.error(request, 'The phone you entered is not your user phone')
            return render(request, 'accounts/password_change_page.html')
        # Verify phone number is present in the user database
        try:
            gambler = GamblerProfile.objects.filter(phone_number=phone_number).first()
        except GamblerProfile.DoesNotExist:
            # If the user is not present, send an error message and redirect to the register page
            return render(request, 'accounts/register.html', {'error_message': 'Nou Pa jwen n Telefòn sa.'})

        # If the user is present, generate the code to send via SMS
        code = code_generator()
         # Your Account SID and Auth Token from Twilio Console
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        
        # Create a Twilio client
        client = Client(account_sid, auth_token)
        
        try:
            # Create and send the SMS
            message = client.messages.create(
            body=f"Kòd pou chanje modpas la: {code}",
            from_=Twillio_PHONE,  # Your Twilio phone number
            to='+509'+phone_number
            )
            print(message)
            expiration_time = datetime.now() + timedelta(minutes=2)

            # Save the code and expiration time in the PasswordChange model
            password_change = PasswordChange.objects.create(
            gambler_id=gambler.profile_id,
            phone_number_for_new_password=phone_number,
            code_generated_for_new_password=code,
            hash_new_password='',
            expiration_time=expiration_time,
            )
            password_change.save()
            return redirect('accounts:code_verification')
        # Redirect the client to the generated_code_password_recovery page

        except Exception as e:
            # SMS failed to send
            return render(request, 'accounts/register.html', {'error_message': 'Nou pa rive voye sms la. Re Eseye ankò.'})

    return render(request, 'accounts/password_change_page.html')

def code_generator():
    # Generate a secure random 6-digit code
    code = str(secrets.randbelow(1000000)).zfill(6)
    return code

def code_verification(request):
    if request.method == 'POST':
        current_user = request.user
        current_user_phone_number = current_user.phone_number
        code_user = request.POST.get('code_enter_by_user')
  
        # Verify that the code generated is the same as the code entered by the user
        try:
            gambler = GamblerProfile.objects.get(phone_number=current_user_phone_number)
            last_password_change = PasswordChange.objects.filter(gambler_id=gambler).order_by('-changed_password_date').first()
            if last_password_change and last_password_change.code_generated_for_new_password == code_user:
                # Check if the code is still valid (has not expired)
                if timezone.now() <= last_password_change.expiration_time:
                    # The entered code matches the last generated code for the user and is still valid
                    #return render(request, 'accounts/password_change_success.html', {'phone_number': phone_number})
                    return redirect('accounts:change_password')
                else:
                    # The entered code is valid, but it has expired
                    return render(request, 'accounts/generated_code_password_recovery.html', {'error_message': 'Kòb la ekspire. Jenere on lot kòd.'})
            else:
                # The entered code does not match or there are no password change records for the user
                return render(request, 'accounts/generated_code_password_recovery.html', {'error_message': 'Invalid code. Please try again.'})
        except GamblerProfile.DoesNotExist:
            # If the user is not present, send an error message and redirect to the register page
            return render(request, 'accounts/register.html', {'error_message': 'Phone number not found.'})

    return render(request, 'accounts/generated_code_password_recovery.html')


def change_password(request):
    print(request.user)
    if request.method == 'POST':
        print(request.user)
        phone_number = request.POST.get('phone_number')
        new_password = request.POST.get('new_password')
        print(phone_number,new_password)
        try:
            gambler = GamblerProfile.objects.filter(phone_number=phone_number).first()

            hashed_password = make_password(new_password)
            gambler.password = hashed_password
            gambler.save()
            print(gambler)
            last_password_change = PasswordChange.objects.filter(gambler_id=gambler).order_by('-changed_password_date').first()
            print(last_password_change)
            if last_password_change:
                last_password_change.hash_new_password = hashed_password
                print(last_password_change)
                last_password_change.save()

            # Redirect the user to a success page or login page
            return render(request, 'accounts/password_change_success.html')
        except GamblerProfile.DoesNotExist:
            # If the user is not present, send an error message and redirect to the register page
            return render(request, 'accounts/register.html', {'error_message': 'Phone number not found.'})
        
    return render(request, 'accounts/new_change_password.html')

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")