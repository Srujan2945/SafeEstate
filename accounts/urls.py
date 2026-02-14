from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('seller-kyc/', views.seller_kyc, name='seller_kyc'),
    path('generate-otp/', views.generate_otp, name='generate_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]