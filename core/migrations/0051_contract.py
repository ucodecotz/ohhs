# Generated by Django 3.0.7 on 2020-09-04 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_auto_20200903_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.TextField()),
                ('agree', models.BooleanField(default=False)),
            ],
        ),
    ]
