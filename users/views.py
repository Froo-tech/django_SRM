from django.shortcuts import render, redirect
import hashlib
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from .models import *
from django.contrib import messages

def orders_profile(request, name):
    if request.method == "POST":
        supplier_name = request.POST.get('supplier_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        state = request.POST.get('state')
        payment_state = request.POST.get('payment_state')

        if supplier_name and start_date and end_date and state and payment_state:
            try:
                order = Order(
                    supplier_name=supplier_name,
                    start_date=start_date,
                    end_date=end_date,
                    state=state,
                    payment_state=payment_state,
                    username=request.user.username,
                )
                order.save()
                messages.success(request, 'Заказ успешно сохранён!')
                return redirect('users:orders_profile', name=name)
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении заказа: {e}')

    all_data = Order.objects.filter(username=request.user.username, supplier_name=name)
    context = {
        'name': name,
        'all_data': all_data
    }

    return render(request, 'users/orders-profile.html', context)
def orders(request):
    context = {}
    if request.method == "POST":
        category = request.POST.get('category')
        contact = request.POST.get('contact')
        name = request.POST.get('name')
        suppliers = Suppliers()
        suppliers.url = f"/users/orders/{name}/"
        suppliers.name = name
        suppliers.contact = contact
        suppliers.category = category
        suppliers.username = request.user.username
        suppliers.save()

    all_data = Suppliers.objects.filter(username=request.user.username)
    context = {
        "all_data": all_data,

    }
    return render(request, "users/orders.html", context)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/users/account/")
        else:
            return render(request, "users/login.html", {"error": "Неправильный логин или пароль"})
    return render(request, "users/login.html")


def account(request):
    contex = {}
    if request.user.is_authenticated:
        username = request.user.username

        email = request.user.email
        contex = {"username":username,
                  "email":email}
    else:
        contex = {'anom':"User is not authenticated"}
    return render(request, 'users/account.html', contex)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_')


        if password != password_confirm:

            return render(request, 'users/register.html',{"error" : "Пожалуйста введите одинаковый пароль"})

        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {"error" : "Пользователь с таким username уже сушествует "})

        if User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {"error" : "Пользователь с таким email уже сушествует"})


        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('/users/account/')


        except Exception as e:
            return render(request, 'users/register.html')

    return render(request, 'users/register.html')

def logout(request):
    auth_logout(request)
    return redirect('/users/login/')

def main(request):
    return render(request, 'users/main-page.html')
