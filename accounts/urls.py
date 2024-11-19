from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,PasswordResetCompleteView, PasswordResetConfirmView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('password_recovery/', views.password_recovery, name='password_reset'),
    path('logout/', views.logout_user, name='logout'),
    path('code_verification/', views.code_verification, name='code_verification'),
    path('change_password/', views.change_password, name='change_password'),
]
