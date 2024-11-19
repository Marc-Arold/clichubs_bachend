from django.urls import path, include
from .views import  get_all_offers, update_offer, delete_offer, get_offer

urlpatterns = [
    path('all/', get_all_offers, name='get_all_offers'),
    path('update/<int:offer_id>/', update_offer, name='update_offer'),
    path('delete/<int:offer_id>/', delete_offer, name='delete_offer'),
    path('offer/<int:offer_id>/', get_offer, name='get_offer'),
    path('horse_race_app/', include('horse_race_app.urls')),
    path('football_app/', include('football_app.urls')),
]
