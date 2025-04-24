from django.urls import path
from .views import user_login, register, account, logout, orders, orders_profile, main, delete_order

app_name = 'users'
urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", register, name="register"),
    path("account/", account, name='account'),
    path('logout/', logout, name='logout'),
    path('orders/', orders, name='orders'),
    path('orders/<str:name>/', orders_profile, name='orders_profile'),
    path('orders/delete/<int:order_id>/', delete_order, name='delete_order'),
    path('', main),
]