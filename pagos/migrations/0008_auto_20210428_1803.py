# Generated by Django 2.2 on 2021-04-28 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0007_factura_estatus2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Islr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(verbose_name='Código Seniat')),
                ('actividad', models.CharField(max_length=150, verbose_name='Actividad')),
                ('Tipo', models.CharField(choices=[('PNR', 'Persona Natural Residente'), ('PNNR', 'Persona Natural No Residente'), ('PJD', 'Persona Jurídica Domiciliada'), ('PJND', 'Persona Jurídica No Domiciliada'), ('PJNCD', 'Persona Jurídica No Constituida Domiciliada')], default='PNR', max_length=5)),
                ('retencion', models.DecimalField(decimal_places=5, max_digits=20, verbose_name='% Base Retención')),
                ('mayoresa', models.DecimalField(decimal_places=5, max_digits=20, verbose_name='Mayores a Bs')),
                ('porcentaje', models.DecimalField(decimal_places=5, max_digits=20, verbose_name='%')),
                ('sustraendo', models.DecimalField(decimal_places=5, max_digits=20, verbose_name='Sustraendo Bs')),
                ('sustraendotipo', models.CharField(max_length=100, verbose_name='Actividad')),
            ],
        ),
        migrations.CreateModel(
            name='iva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('porcentaje', models.DecimalField(decimal_places=5, max_digits=20, verbose_name='iva')),
            ],
        ),
        migrations.RemoveField(
            model_name='factura',
            name='monto',
        ),
        migrations.AddField(
            model_name='factura',
            name='big',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='BIG'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factura',
            name='excento',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20, verbose_name='excento'),
            preserve_default=False,
        ),
    ]
