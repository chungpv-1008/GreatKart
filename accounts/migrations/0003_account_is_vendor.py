# Generated by Django 3.2 on 2023-09-04 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_vendor',
            field=models.BooleanField(default=False),
        ),
    ]