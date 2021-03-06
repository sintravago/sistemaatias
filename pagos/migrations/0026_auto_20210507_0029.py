# Generated by Django 2.2 on 2021-05-07 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0025_auto_20210506_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='anticipo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='anticipo',
            name='factura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='get_factura', to='pagos.factura', verbose_name='Factura'),
        ),
    ]
