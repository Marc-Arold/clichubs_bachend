from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_fooball_page, name='fotball_page'),
    path('countries/', views.get_countries, name='countries'),
    path('leagues/', views.get_leagues, name='leagues'),
    #path('odds/', views.get_odds, name='odds_for_a_week'),
    path('fixures/', views.get_fixures_for_a_week, name='fixures_for_a_week'),
]
