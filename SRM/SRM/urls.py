
from django.contrib import admin
from django.urls import path, include
app_name = 'users'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls"), name="users"),

]
