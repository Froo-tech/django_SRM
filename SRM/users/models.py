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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=15)

class Suppliers(models.Model):
    name = models.TextField()
    contact = models.CharField(max_length=15)
    category = models.CharField(max_length=40)

class Order(models.Model):
    supplier_name = models.TextField()
    start_date = models.DateField()
    end_date = models.TextField()
    payment_terms = models.TextField()

