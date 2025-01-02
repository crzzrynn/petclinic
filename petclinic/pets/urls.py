from django.urls import path, include
from . import views
from .views import (
    client_list, create_client, edit_client, delete_client,
    pet_list, create_pet, edit_pet, delete_pet,
    appointment_list, create_appointment, edit_appointment, delete_appointment,
    article_list, create_article, edit_article, delete_article,
    medical_record_list, create_medical_record, edit_medical_record, delete_medical_record,CustomLoginView
)


urlpatterns = [
    
    # Homepage Url
    path('', views.home, name='home'),

    # Login/Register Urls
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Client URLs
    path('clients/', client_list, name='client_list'),
    path('clients/create/', create_client, name='create_client'),
    path('clients/edit/<int:client_id>/', edit_client, name='edit_client'),
    path('clients/delete/<int:client_id>/', delete_client, name='delete_client'),

    # Pet URLs
    path('pets/', pet_list, name='pet_list'),
    path('pets/create/', create_pet, name='create_pet'),
    path('pets/edit/<int:pet_id>/', edit_pet, name='edit_pet'),
    path('pets/delete/<int:pet_id>/', delete_pet, name='delete_pet'),

    # Appointment URLs
    path('appointments/', appointment_list, name='appointment_list'),
    path('appointments/create/', create_appointment, name='create_appointment'),
    path('appointments/edit/<int:appointment_id>/', edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),

    # Article URLs
    path('articles/', article_list, name='article_list'),
    path('articles/create/', create_article, name='create_article'),
    path('articles/edit/<int:article_id>/', edit_article, name='edit_article'),
    path('articles/delete/<int:article_id>/', delete_article, name='delete_article'),

    # Medical Record URLs
    path('medical-records/', medical_record_list, name='medical_record_list'),
    path('medical-records/create/', create_medical_record, name='create_medical_record'),
    path('medical-records/edit/<int:record_id>/', edit_medical_record, name='edit_medical_record'),
    path('medical-records/delete/<int:record_id>/', delete_medical_record, name='delete_medical_record'),

]