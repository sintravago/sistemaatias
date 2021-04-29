from django.db import models
from registration.models import departamento
from datetime import datetime

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'rif_{0}/{1}'.format(instance.rif, filename)
    
# Create your models here.
class factura(models.Model):
    choise_estatus = [
        ('R', 'Registrada'),
        ('S', 'Seleccionada'),
        ('A', 'Aprobada'),
        ('P', 'Pagada'),
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
    big = models.DecimalField(verbose_name='BIG', max_digits=20, decimal_places=5)
    excento = models.DecimalField(verbose_name='excento', max_digits=20, decimal_places=5)
    iva = models.DecimalField(verbose_name='IVA', max_digits=20, decimal_places=5)
    islr = models.DecimalField(verbose_name='ISLR', max_digits=20, decimal_places=5)
    gerencia = models.ForeignKey(departamento, verbose_name="Gerencia", on_delete=models.CASCADE)
    direccion = models.TextField(verbose_name='Dirección Corporativa')
    archivo = models.FileField(upload_to=user_directory_path, null=True,  blank=True)
    estatus = models.BooleanField(default=False)
    estatus2 = models.BooleanField(default=False)

    def antiguedad(self):
        return (datetime.now().date() - self.fecharecepcion)
    
    def total(self):
        return self.big + self.iva + self.excento

class iva(models.Model):
    porcentaje = models.DecimalField(verbose_name='iva', max_digits=20, decimal_places=5)

    def __str__(self):
        return self.porcentaje

class Islr(models.Model):
    choise_tipo = [
        ('PNR', 'Persona Natural Residente'),
        ('PNNR', 'Persona Natural No Residente'),
        ('PJD', 'Persona Jurídica Domiciliada'),
        ('PJND', 'Persona Jurídica No Domiciliada'),
        ('PJNCD', 'Persona Jurídica No Constituida Domiciliada'),
    ]
    codigo = models.IntegerField(verbose_name='Código Seniat')
    actividad = models.CharField(max_length=150 , verbose_name='Actividad')
    Tipo = models.CharField(max_length=5, choices=choise_tipo, default='PNR')
    retencion = models.DecimalField(verbose_name='% Base Retención', max_digits=20, decimal_places=5)
    mayoresa = models.DecimalField(verbose_name='Mayores a Bs', max_digits=20, decimal_places=5)
    porcentaje = models.DecimalField(verbose_name='%', max_digits=20, decimal_places=5)
    sustraendo = models.DecimalField(verbose_name='Sustraendo Bs', max_digits=20, decimal_places=5)
    sustraendotipo = models.CharField(max_length=100 , verbose_name='Actividad')

    def __str__(self):
        return self.codigo