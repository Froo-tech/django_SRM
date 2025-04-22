from django.contrib import admin
from django.urls import path
from .views import *


app_name = 'users'
urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", register),
    path("account/", account, name='account'),
    path('logout/', logout, name='logout'),
    path('orders/', orders, name='orders'),
    path('orders/<str:name>/', orders_profile, name='orders_profile'),
    path('', main),
]
