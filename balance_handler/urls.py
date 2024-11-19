from django.urls import path
from . import views

urlpatterns = [
    path("", views.balance_handler),
    path("balances/", views.balance, name='balances'),
    path('bonus_conversion/', views.conversion_bonus, name='bonus_conversion')
]

