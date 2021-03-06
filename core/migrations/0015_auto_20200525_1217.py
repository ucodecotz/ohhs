# Generated by Django 3.0.6 on 2020-05-25 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0014_auto_20200522_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedlabour',
            name='selected_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('labour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.LaboursProfile')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'comments',
            },
        ),
    ]
