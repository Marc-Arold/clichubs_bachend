from django.urls import path
from . import views

urlpatterns = [
     path('', views.withdrawal, name='withdrawal'),
    path('list/', views.withdrawal_list, name='withdrawal_list'),
    path('create/', views.withdraw_moncash, name='withdrawal_create'),
    path('withdrawal_list_for_current_user/', views.withdrawal_list_for_current_user, name='withdrawal_list_for_current_user')
]