# Generated by Django 3.2 on 2023-09-04 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('P', 'paypal'), ('M', 'momo'), ('C', 'cod')], default='PENDING', max_length=1),
        ),
    ]