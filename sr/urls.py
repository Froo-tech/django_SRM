from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', tasks),
    path('analytics/', analytics),

    path('', index),

]
