from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.deposit),
    path('list_deposit_companies/', login_required(views.deposit_list_for_current_user), name='deposit_list_for_current_user_companies'),
    path('moncash_companies/', views.deposit_moncash, name='deposit_moncash_companies'),
    path('moncash/callback/', login_required(views.deposit_callback), name='deposit_return_url_moncash'),
]
