# Generated by Django 2.2 on 2021-04-29 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0011_auto_20210429_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='cambiofactura',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='Cambio Factura'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factura',
            name='cambiopago',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='Cambio Pago'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factura',
            name='islr',
            field=models.DecimalField(decimal_places=5, default=75, max_digits=20, verbose_name='ISL'),
        ),
        migrations.AddField(
            model_name='factura',
            name='retiva',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='Ret. IVA'),
        ),
        migrations.AlterField(
            model_name='iva',
            name='porcentaje',
            field=models.DecimalField(decimal_places=5, max_digits=20, verbose_name='IVA'),
        ),
    ]
