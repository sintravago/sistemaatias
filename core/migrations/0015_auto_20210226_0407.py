# Generated by Django 2.2 on 2021-02-26 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210226_0226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guardia',
            name='fecha',
        ),
        migrations.AlterField(
            model_name='guardia',
            name='entrada',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='guardia',
            name='salida',
            field=models.DateField(),
        ),
    ]