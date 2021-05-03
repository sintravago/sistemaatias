# Generated by Django 2.2 on 2021-04-30 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0014_auto_20210430_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='islr',
            name='mayoresa',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True, verbose_name='Mayores a Bs'),
        ),
        migrations.AlterField(
            model_name='islr',
            name='porcentaje',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True, verbose_name='%'),
        ),
        migrations.AlterField(
            model_name='islr',
            name='retencion',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True, verbose_name='% Base Retención'),
        ),
        migrations.AlterField(
            model_name='islr',
            name='sustraendo',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True, verbose_name='Sustraendo Bs'),
        ),
        migrations.AlterField(
            model_name='islr',
            name='sustraendotipo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Actividad'),
        ),
    ]