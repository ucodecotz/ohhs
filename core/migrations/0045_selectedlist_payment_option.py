# Generated by Django 3.0.7 on 2020-08-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_address_payment_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedlist',
            name='payment_option',
            field=models.CharField(blank=True, choices=[('V', 'Vodacom'), ('A', 'Airtel')], max_length=200, null=True),
        ),
    ]
