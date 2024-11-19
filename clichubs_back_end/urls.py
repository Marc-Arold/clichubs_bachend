from django.contrib import admin
from django.urls import path, include
from . import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('withdrawals/', include('withdrawals.urls')),
    path('deposit/', include('deposit.urls')),
    path('deposit_companies/', include('deposit_companies.urls')),
    path('companies_accounts/', include('companies_accounts.urls')),
    path('balance_handler/', include('balance_handler.urls')),
    path('balance_handler_companies/', include('balance_handler_companies.urls')),
    path('withdrawals_companies/', include('withdrawals_companies.urls')),
    path('offers/', include('offers.urls')),
   
   
]
