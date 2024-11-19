# Create your views here.
from django.shortcuts import render
from .models import BalanceCompanies
from companies_accounts.models import CompanyProfile
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# Create your views here.
@login_required
def balance_handler(request):
    return render(request, 'balance_company.html')

@login_required
def balance(request):
    current_user_patent_number = request.user.patent_number
    
    company_profile = CompanyProfile.objects.get(patent_number=current_user_patent_number)

    balance_user = BalanceCompanies.objects.filter(company=company_profile).order_by('-balance_date').first()

    balance_globale = balance_user.balance_globale

    #balance_company = JsonResponse(balance_globale)
    print(balance_globale)
    return render(request, 'balances_company.html', context=balance_globale)