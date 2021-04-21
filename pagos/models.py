from django.db import models
from registration.models import departamento

# Create your models here.
class factura(models.Model):
    choise_estatus = [
        ('R', 'Registrado'),
        ('S', 'Seleccionado'),
        ('P', 'Pre-aprobado'),
        ('A', 'Aprobado'),
    ]

    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')
    rif = models.CharField(max_length=150 , verbose_name='RIF')
    razon = models.CharField(max_length=150 , verbose_name='Razón Social')
    nfactura = models.IntegerField(verbose_name='Número de Factura')
    ncontrol = models.IntegerField(verbose_name='Número de Control')
    fechafactura = models.DateField(verbose_name='Fecha de Factura')
    fecharecepcion = models.DateField(verbose_name='Fecha de Recepción')
    concepto = models.CharField(max_length=150 , verbose_name='Concepto')
    monto = models.DecimalField(verbose_name='Monto', max_digits=20, decimal_places=5)
    iva = models.DecimalField(verbose_name='IVA', max_digits=20, decimal_places=5)
    islr = models.DecimalField(verbose_name='ISLR', max_digits=20, decimal_places=5)
    gerencia = models.ForeignKey(departamento, verbose_name="Gerencia", on_delete=models.CASCADE)
    direccion = models.TextField(verbose_name='Dirección Corporativa')
    estatus = models.CharField(max_length=1, choices=choise_estatus, default='R')

