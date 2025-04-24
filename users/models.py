from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage

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
    order_type = models.TextField(default="Обычный")
    created_at = models.DateTimeField(auto_now=True)
    file_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

class OrderFile(models.Model):
    order = models.ForeignKey(Order, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='orders/files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=OrderFile)
def update_order_file_url(sender, instance, created, **kwargs):
    if created and instance.file:
        file_url = default_storage.url(instance.file.name)
        instance.order.file_url = file_url
        instance.order.save()