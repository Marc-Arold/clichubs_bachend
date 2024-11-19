from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.deposit),
    path('list_deposit/', login_required(views.deposit_list_for_current_user), name='deposit_list_for_current_user'),
    path('moncash/', views.deposit_moncash, name='deposit_moncash'),
    path('moncash/callback/', login_required(views.deposit_callback), name='deposit_return_url_moncash'),
]
