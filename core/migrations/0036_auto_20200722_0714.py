# Generated by Django 3.0.7 on 2020-07-22 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20200721_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboursprofile',
            name='work',
            field=models.CharField(blank=True, max_length=29, null=True),
        ),
    ]
