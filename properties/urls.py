from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('add/', views.add_property, name='add_property'),
    path('<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('<int:pk>/manage-images/', views.manage_property_images, name='manage_property_images'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('<int:pk>/request-visit/', views.request_visit, name='request_visit'),
    path('visit-request/<int:pk>/respond/', views.respond_visit_request, name='respond_visit_request'),
    path('my-visit-requests/', views.my_visit_requests, name='my_visit_requests'),
]