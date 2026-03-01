from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report-lost-pet/', views.report_lost_pet, name='report_lost_pet'),
    path('report-found-pet/', views.report_found_pet, name='report_found_pet'),
    path('adoption/', views.adoption_form, name='adoption_form'),
    path('lost-pets/', views.lost_pets_list, name='lost_pets_list'),
    path('found-pets/', views.found_pets_list, name='found_pets_list'),
    path('adoption-list/', views.adoption_list, name='adoption_list'),
    path('pet/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pet/<int:pk>/adopt/', views.submit_adoption_request, name='submit_adoption_request'),
    path('manage-adoption-requests/', views.admin_adoption_requests, name='admin_adoption_requests'),
    path('admin/approve-request/<int:pk>/', views.approve_adoption_request, name='approve_adoption_request'),
    path('admin/reject-request/<int:pk>/', views.reject_adoption_request, name='reject_adoption_request'),
]
