from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    tel = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "tel", "password1", "password2")


class Images(models.Model):
    img = models.ImageField(upload_to='article', height_field=100, width_field=100)

class Profile(models.Model):
    username = models.TextField(default="None")
    tel = models.CharField(max_length=15)

class Suppliers(models.Model):
    username = models.TextField(default="None")
    name = models.TextField()
    contact = models.CharField(max_length=15)
    category = models.CharField(max_length=40)
    url = models.TextField(default="None")

class Order(models.Model):
    username = models.TextField(default="None")
    supplier_name = models.TextField(default="none")
    start_date = models.DateField(default="None")
    end_date = models.DateField(default="None")
    state = models.CharField(max_length=40, default="None")
    payment_state = models.TextField(default="None")


