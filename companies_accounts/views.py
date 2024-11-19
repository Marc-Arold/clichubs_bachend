# companies_accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .models import CompanyProfile, OwnerTable
from .forms import CompanyRegistrationForm, OwnerTableForm,CompanyLoginForm
from django.contrib import messages
from .authentication_backends import CompanyAuthBackend
from django.contrib.auth.hashers import make_password
import random
import string
from django.http import JsonResponse


def home_page_company(request):
    print(request.user)
    return render(request, 'companies_accounts/home_page_company.html')


def create_company(request):
    if request.method == 'POST':
        owner_form = OwnerTableForm(request.POST)
        
        if owner_form.is_valid():
            owner = owner_form.save()
            return redirect('create_company_profile', owner_id=owner.pk)  # change this part
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        owner_form = OwnerTableForm()

    return render(request, 'companies_accounts/create_owner.html', {'owner_form': owner_form})


def create_company_profile(request, owner_id):
    owner = OwnerTable.objects.get(pk=owner_id)
    if request.method == 'POST':
        company_form = CompanyRegistrationForm(request.POST)
        patent_number = generate_patent_number()
        if company_form.is_valid():
            raw_password = company_form.cleaned_data.get('password1')
            hashed_password = make_password(raw_password)
            company = company_form.save(commit=False)
            company.owner = owner
            company.patent_number = patent_number
            company.company_type = 'SMALL'
            company.hash_password = hashed_password
            company.save()
            return redirect('company_login')
          
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        company_form = CompanyRegistrationForm()

    return render(request, 'companies_accounts/create_company.html', {'company_form': company_form, 'owner': owner})




def generate_patent_number():
    length = 10  # Define the length of the patent number

    while True:
        # Generate a random alphanumeric string of defined length
        patent_number = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # Check if the patent number already exists in the CompanyProfile model
        if not CompanyProfile.objects.filter(patent_number=patent_number).exists():
            return patent_number



def update_owner_info(request):
    owner = get_object_or_404(OwnerTable, owner_id=request.user.owner.id)

    if request.method == 'POST':
        form = OwnerTableForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Owner information updated successfully.')
        else:
            messages.error(request, 'Invalid form submission. Please check the form and try again.')

    else:
        form = OwnerTableForm(instance=owner)

    return render(request, 'companies_accounts/update_owner_info.html', {'form': form})

def company_login(request):
    
    if 'gambler' in request.session:
        del request.session['gambler']
    
    if request.method == 'POST':
        patent_number = request.POST.get('patent_number')
        password = request.POST.get('password')
       
    
        # Authenticate the company using the custom authentication backend
        backend = CompanyAuthBackend()
        user = backend.authenticate(request, patent_number=patent_number, password=password)
        user = backend.get_user(patent_number=patent_number)
        if user:
            user.backend = 'clichubs_back_end.companies_accounts.authentication_backends.CompanyAuthBackend'
            login(request, user)
            request.session['role'] = 'company'
            return redirect('company_dashboard')  # Change 'company_dashboard' to the URL name of the company's dashboard view
        else:
            # Invalid credentials
            messages.error(request, 'Invalid patent number or password.')
  
    return render(request, 'companies_accounts/company_login.html') 

def dashboard(request):
    print(request.user)
    return render(request, 'companies_accounts/dashboard_company.html')