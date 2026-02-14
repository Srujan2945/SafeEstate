from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('properties/', views.manage_properties, name='manage_properties'),
    path('kyc/', views.kyc_verification, name='kyc_verification'),
    path('kyc/<int:pk>/', views.kyc_detail, name='kyc_detail'),
    path('user/<int:pk>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('property/<int:pk>/toggle-status/', views.toggle_property_status, name='toggle_property_status'),
    path('images/', views.manage_property_images, name='manage_property_images'),
    path('images/bulk-assign/', views.bulk_assign_images, name='bulk_assign_images'),
]