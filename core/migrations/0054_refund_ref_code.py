# Generated by Django 3.0.7 on 2020-09-14 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20200905_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='refund',
            name='ref_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
