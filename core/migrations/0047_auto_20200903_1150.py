# Generated by Django 3.0.7 on 2020-09-03 11:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0046_auto_20200826_0650'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='selectedList',
            new_name='LabourSelectedList',
        ),
    ]
