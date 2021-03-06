# Generated by Django 3.0.6 on 2020-05-21 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_auto_20200521_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboursprofile',
            name='location',
            field=models.CharField(choices=[('AR', 'Arusha'), ('DA', 'Dar es salaam')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='laboursprofile',
            name='phone',
            field=models.CharField(max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='laboursprofile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
