# Generated by Django 5.2 on 2025-04-19 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_rename_order_orderfile_order_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderfile',
            old_name='order_id',
            new_name='order',
        ),
    ]
