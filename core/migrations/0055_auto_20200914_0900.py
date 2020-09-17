# Generated by Django 3.0.7 on 2020-09-14 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0054_refund_ref_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refund',
            name='selected_labour',
        ),
        migrations.AddField(
            model_name='refund',
            name='made_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
