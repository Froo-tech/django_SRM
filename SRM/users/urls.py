from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("login/", user_login),
    path("register/", register),
    path("account/", account),
    path('logout/', logout),  
    path('orders/', orders),
    path('', main),
]
