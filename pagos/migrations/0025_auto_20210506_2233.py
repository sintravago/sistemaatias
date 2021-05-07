# Generated by Django 2.2 on 2021-05-06 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pagos', '0024_auto_20210505_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pagos.Empresa', verbose_name='Proveedor'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='tipo',
            field=models.CharField(choices=[('ser', 'Servicio'), ('alm', 'Compra de almacén'), ('dir', 'Compra directa')], default='ser', max_length=3, verbose_name='Tipo de Factura'),
        ),
        migrations.CreateModel(
            name='anticipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('fechapago', models.DateField(blank=True, null=True, verbose_name='Fecha de Pago')),
                ('montobs', models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='BS')),
                ('montousd', models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='USD')),
                ('cambio', models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='Tipo de cambio')),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pagos.factura', verbose_name='Factura')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]
