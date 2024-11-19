from django.urls import path
from . import views

urlpatterns = [
    path("", views.balance_handler),
    path("balances_company/", views.balance, name='balances_company'),
    
]
 