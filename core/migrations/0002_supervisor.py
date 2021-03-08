# Generated by Django 2.2 on 2021-03-08 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0002_auto_20210308_1327'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='get_departamento', to='registration.departamento', verbose_name='Departamento')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='get_user_d', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]
