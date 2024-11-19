from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page_company, name='create_company'),
    path('company_dashboard/', views.dashboard, name='company_dashboard'),
    path('create/', views.create_company, name='create_company'),
    path('create_company_profile/<int:owner_id>/', views.create_company_profile, name='create_company_profile'),
    path('company_login/', views.company_login, name='company_login'),
    path('update_owner_info/', views.update_owner_info, name='update_owner_info'),
    # Add more URLs for other views as needed
]
