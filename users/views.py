import json
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from .models import *
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Order, OrderFile
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from .models import Order
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_')
        logger.info(f"Data was successfully received for register:{username}")


        if password != password_confirm:
            logger.info(f"Please enter the same password:{username}")
            return render(request, 'users/register.html',{"error" : "Пожалуйста введите одинаковый пароль"})

        if User.objects.filter(username=username).exists():
            logger.info(f"A user with this username already exists:{username}")
            return render(request, 'users/register.html', {"error" : "Пользователь с таким username уже существует "})

        if User.objects.filter(email=email).exists():
            logger.info(f"The user with this email already exists:{username}")
            return render(request, 'users/register.html', {"error" : "Пользователь с таким email уже существует"})


        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            logger.info(f"User has been successfully registered:{username}")
            return redirect('/users/account/')


        except Exception as e:
            return render(request, 'users/register.html')

    return render(request, 'users/register.html')

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
        logger.info(f"Data was successfully received for orders:{request.user.username}")
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
            logger.warning(f"Incorrect username or password: {username}")
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
        logger.info('User is not authenticated')
        contex = {'anom':"User is not authenticated"}
    return render(request, 'users/account.html', contex)

@login_required
def orders_profile(request, name):
    if request.method == "POST":
        try:
            order = Order(
                username=request.user.username,
                supplier_name=name,
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                state=request.POST.get('state'),
                payment_state=request.POST.get('payment_state'),
                order_type=request.POST.get('order_type')
            )
            order.save()
            logger.info(f"Data was successfully received for create order:{request.user.username}")

            files = request.FILES.getlist('files')
            for file in files:
                OrderFile.objects.create(order=order, file=file)
            logger.info('The order was successfully created')
            messages.success(request, 'Заказ успешно создан')
            return redirect('users:orders_profile', name=name)

        except Exception as e:
            messages.error(request, f'Ошибка при сохранении заказа: {e}')

    orders = Order.objects.filter(
        username=request.user.username,
        supplier_name=name
    ).order_by('-created_at').prefetch_related('files')

    orders_data = []
    for order in orders:
        files_data = [
            {
                'url': default_storage.url(file.file.name),
                'name': file.file.name.split('/')[-1],
                'uploaded_at': file.uploaded_at
            }
            for file in order.files.all()
        ]

        main_file_url = files_data[0]['url'] if files_data else None
        main_file_name = files_data[0]['name'] if files_data else None

        orders_data.append({
            'order': order,
            'files': files_data,
            'main_file_url': main_file_url,
            'main_file_name': main_file_name
        })

    context = {
        'name': name,
        'orders_data': orders_data,
        'orders_data_json': json.dumps([{
            'order': {
                'id': data['order'].id,
                'username': data['order'].username,
                'start_date': data['order'].start_date.strftime('%Y-%m-%d'),
                'end_date': data['order'].end_date.strftime('%Y-%m-%d'),
                'state': data['order'].state,
                'payment_state': data['order'].payment_state,
                'order_type' : data['order'].order_type
            },
            'files': [{
                'url': file['url'],
                'name': file['name'],
                'uploaded_at': file['uploaded_at'].strftime('%Y-%m-%d %H:%M:%S')
            } for file in data['files']],
            'main_file_url': data['main_file_url'],
            'main_file_name': data['main_file_name']
        } for data in orders_data], default=str)
    }
    return render(request, 'users/orders-profile.html', context)


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        username=request.user.username
    )

    for file in order.files.all():
        file.file.delete()
        file.delete()
    order.delete()
    logger.info(f'The order was successfully deleted:{order_id}')

    next_url = request.META.get('HTTP_REFERER')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()}
    ):
        return redirect(next_url)
    return redirect('users:orders')

@login_required
def delete_suppliers(request, supplier_id):
    supplier = get_object_or_404(Suppliers, id=supplier_id)
    if supplier.username != request.user.username:
        return HttpResponseForbidden()
    supplier.delete()
    logger.info(f'The suppliers was successfully deleted:{supplier_id}')

    return redirect(request.META.get('HTTP_REFERER', 'users:orders'))

def logout(request):
    logger.info(f'The user logged out of the account{request.user.username}')
    auth_logout(request)
    return redirect('/users/login/')

def main(request):
    return render(request, 'users/main-page.html')

