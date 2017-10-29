from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^home/', views.get_user_list, name='index'),
    url(r'^store/', views.save_data, name='savedata'),
    url(r'^alert/', views.send_alert, name='sendalert'),
    url(r'^alert2/', views.send_alert2, name='sendalert'),

    url(r'^savemedicines/', views.save_medicines_data, name='savemedicinesdata'),
    url(r'^savemedicines2/', views.save_medicines_data2, name='savemedicinesdata2'),

    url(r'^getuserlist/', views.get_user_list, name='getuserlist'),
    url(r'^getusermedicines/', views.get_user_medicines, name='getusermedicines'),
    url(r'^get2usermedicines/', views.get_user_medicines_get, name='get2usermedicines'),

    url(r'^users/', views.list_users.as_view(), name='users'),
    url(r'^userdetails/', views.user_details.as_view(), name='userdetails'),
    url(r'^addprescription/', views.add_user_prescription.as_view(), name='addprescription'),

]
