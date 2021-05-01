# Generated by Django 2.2 on 2021-04-30 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0016_factura_tiposervicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='big',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='BIG'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='cambiofactura',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='Tipo de cambio (factura)'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='cambiopago',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='Tipo de cambio (fecha de pago)'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='divisa',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='A pagar en USD'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='exento',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='Exento'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='islr',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='ISL'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='iva',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='IVA'),
        ),
    ]
