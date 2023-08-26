# Generated by Django 3.2 on 2023-08-09 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20230808_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('estimated_delivery_time', models.CharField(max_length=50)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('tracking_number', models.CharField(blank=True, max_length=20)),
                ('tracking_url', models.CharField(blank=True, max_length=100)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_id', to='orders.order')),
                ('shipping_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.shippingmethod')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_id', to='orders.shipping'),
        ),
    ]