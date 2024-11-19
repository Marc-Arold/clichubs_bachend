from django.urls import path
from .views import  create_horse_race,get_horse_races_by_company,create_selection

urlpatterns = [
    path('horse_races/<int:company_id>/', get_horse_races_by_company, name='get_all_horce_races_by_company'),
    path('create_horse_race/', create_horse_race, name='create_horse_race'),
    path('select_horse_race/', create_selection, name='select_horse_race'),
   
]
