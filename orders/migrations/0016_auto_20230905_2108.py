# Generated by Django 3.2 on 2023-09-05 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20230905_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='order_payment',
        ),
        migrations.RemoveField(
            model_name='shipping',
            name='order',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='orders.payment'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='orders.shipping'),
        ),
    ]
