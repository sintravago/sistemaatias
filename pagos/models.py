from django.db import models
from registration.models import departamento
from datetime import datetime
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'rif_{0}/{1}'.format(instance.rif, filename)
    
# Create your models here.

class Empresa(models.Model):
    choise_clasificacion = [
        ('PNR', 'Persona Natural Residente'),
        ('PNNR', 'Persona Natural No Residente'),
        ('PJD', 'Persona Jurídica Domiciliada'),
        ('PJND', 'Persona Jurídica No Domiciliada'),
        ('PJNCD', 'Persona Jurídica No Constituida Domiciliada'),
    ]
    choise_rift = [
        ('V', 'V'),
        ('E', 'E'),
        ('P', 'P'),
        ('J', 'J'),
        ('G', 'G'),
    ]
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT) 
    rif = models.IntegerField(verbose_name='RIF')
    rift = models.CharField(max_length=1, choices=choise_rift, default='J')
    razon = models.CharField(max_length=150 , verbose_name='Razón Social')
    clasificacion = models.CharField(max_length=5, choices=choise_clasificacion, default='PNR')
    direccion = models.TextField(verbose_name='Dirección Corporativa', null = True, blank = True)
    tlf = models.CharField(max_length=50 , verbose_name='Teléfono', null = True, blank = True)

    def __str__(self):
        return "{} ({}-{})".format(self.razon, self.rift, self.rif)

class factura(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT) 
    empresa = models.ForeignKey(Empresa, verbose_name="Empresa", on_delete=models.PROTECT)
    nfactura = models.CharField(max_length=150, verbose_name='Número de Factura')
    ncontrol = models.IntegerField(verbose_name='Número de Control')
    fechafactura = models.DateField(verbose_name='Fecha de Factura')
    fecharecepcion = models.DateField(verbose_name='Fecha de Recepción')
    concepto = models.CharField(max_length=150 , verbose_name='Concepto')
    big = models.DecimalField(verbose_name='BIG', max_digits=20, decimal_places=5)
    exento = models.DecimalField(verbose_name='Exento', max_digits=20, decimal_places=5)
    iva = models.DecimalField(verbose_name='IVA', max_digits=20, decimal_places=5)
    islr = models.DecimalField(verbose_name='ISL', max_digits=20, decimal_places=5, default=75)
    retiva = models.DecimalField(verbose_name='Ret. IVA', max_digits=20, decimal_places=5, default=0)
    cambiofactura = models.DecimalField(verbose_name='Cambio Factura', max_digits=20, decimal_places=5)
    cambiopago = models.DecimalField(verbose_name='Cambio Pago', max_digits=20, decimal_places=5)
    archivo = models.FileField(upload_to=user_directory_path, null=True,  blank=True)
    estatus = models.BooleanField(default=False)
    estatus2 = models.BooleanField(default=False)

    def antiguedad(self):
        return (datetime.now().date() - self.fecharecepcion)
    
    def total(self):
        return self.big + self.iva + self.exento

class iva(models.Model):
    porcentaje = models.DecimalField(verbose_name='IVA', max_digits=20, decimal_places=5)

    def __str__(self):
        return self.porcentaje

class Islr(models.Model):
    choise_clasificacion = [
        ('PNR', 'Persona Natural Residente'),
        ('PNNR', 'Persona Natural No Residente'),
        ('PJD', 'Persona Jurídica Domiciliada'),
        ('PJND', 'Persona Jurídica No Domiciliada'),
        ('PJNCD', 'Persona Jurídica No Constituida Domiciliada'),
    ]
    codigo = models.IntegerField(verbose_name='Código Seniat')
    actividad = models.CharField(max_length=150 , verbose_name='Actividad')
    Tipo = models.CharField(max_length=5, choices=choise_clasificacion, default='PNR')
    retencion = models.DecimalField(verbose_name='% Base Retención', max_digits=20, decimal_places=5)
    mayoresa = models.DecimalField(verbose_name='Mayores a Bs', max_digits=20, decimal_places=5)
    porcentaje = models.DecimalField(verbose_name='%', max_digits=20, decimal_places=5)
    sustraendo = models.DecimalField(verbose_name='Sustraendo Bs', max_digits=20, decimal_places=5)
    sustraendotipo = models.CharField(max_length=100 , verbose_name='Actividad')

    def __str__(self):
        return self.codigo