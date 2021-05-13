from django.db import models
from registration.models import departamento
from datetime import datetime
from django.contrib.auth.models import User
import math

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'rif_{0}/{1}'.format(instance.empresa.rif, filename)
    
# Create your models here.

class Islr(models.Model):
    choise_clasificacion = [
        ('PNR', 'Persona Natural Residente'),
        ('PNNR', 'Persona Natural No Residente'),
        ('PJD', 'Persona Jurídica Domiciliada'),
        ('PJND', 'Persona Jurídica No Domiciliada'),
        ('PJNCD', 'Persona Jurídica No Constituida Domiciliada'),
    ]
    codigo = models.IntegerField(verbose_name='Código Seniat')
    actividad = models.CharField(max_length=250 , verbose_name='Actividad')
    Tipo = models.CharField(max_length=5, choices=choise_clasificacion, default='PNR')
    retencion = models.DecimalField(verbose_name='% Base Retención', max_digits=20, decimal_places=5, null=True,  blank=True)
    mayoresa = models.DecimalField(verbose_name='Mayores a Bs', max_digits=20, decimal_places=5, null=True,  blank=True)
    porcentaje = models.DecimalField(verbose_name='%', max_digits=20, decimal_places=5, null=True,  blank=True)
    sustraendo = models.DecimalField(verbose_name='Sustraendo Bs', max_digits=20, decimal_places=5, default = 0)
    sustraendotipo = models.CharField(max_length=100 , verbose_name='Actividad', null=True,  blank=True)

    def __str__(self):
        return "{}".format(self.codigo)
    
    def descript(self):
        return "{} : {}".format(self.codigo, self.actividad)

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
    choise_iva = [
        (0,0),
        (75, 75),
        (100, 100),
    ]
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT) 
    rif = models.CharField(verbose_name='RIF', max_length=150)
    rift = models.CharField(max_length=1, choices=choise_rift, default='J')
    razon = models.CharField(max_length=150 , verbose_name='Razón Social')
    clasificacion = models.CharField(max_length=5, choices=choise_clasificacion, default='PNR')
    retiva = models.IntegerField(verbose_name='Retención IVA', choices=choise_iva, default=75)
    direccion = models.TextField(verbose_name='Dirección Corporativa', null = True, blank = True)
    tlf = models.CharField(max_length=50 , verbose_name='Teléfono', null = True, blank = True)

    def __str__(self):
        return "{} ({}-{})".format(self.razon, self.rift, self.rif)

class factura(models.Model):
    choise_tipo = [
        ('ser', 'Servicio'),
        ('alm', 'Compra de almacén'),
        ('dir', 'Compra directa'),
    ]

    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT) 
    empresa = models.ForeignKey(Empresa, verbose_name="Proveedor", on_delete=models.PROTECT)
    nfactura = models.CharField(max_length=150, verbose_name='Número de Factura')
    ncontrol = models.CharField(max_length=150, verbose_name='Número de Control')
    fechafactura = models.DateField(verbose_name='Fecha de Factura')
    fecharecepcion = models.DateField(verbose_name='Fecha de Recepción')
    fechapago = models.DateField(verbose_name='Fecha de Pago', null=True,  blank=True)
    concepto = models.CharField(max_length=150 , verbose_name='Concepto')
    big = models.DecimalField(verbose_name='BIG', max_digits=20, decimal_places=5, default=0)
    exento = models.DecimalField(verbose_name='Exento', max_digits=20, decimal_places=5, default=0)
    iva = models.DecimalField(verbose_name='IVA', max_digits=20, decimal_places=5, default=0)
    retiva = models.IntegerField(verbose_name='Retención IVA', default=75)
    islr = models.DecimalField(verbose_name='ISL', max_digits=20, decimal_places=5, default=0)
    sustraendo = models.DecimalField(verbose_name='Sustraendo', max_digits=20, decimal_places=5, default=0)
    cambiofactura = models.DecimalField(verbose_name='Tipo de cambio (factura)', max_digits=20, decimal_places=5, default = 0)
    cambiopago = models.DecimalField(verbose_name='Tipo de cambio (fecha de pago)', max_digits=20, decimal_places=5, default = 0)
    divisa = models.DecimalField(verbose_name='A pagar en USD', max_digits=20, decimal_places=5, default=0)
    archivo = models.FileField(upload_to=user_directory_path, null=True,  blank=True)
    estatus = models.BooleanField(default=False)
    estatus2 = models.BooleanField(default=False)
    estatus3 = models.BooleanField(default=False)
    anticipo = models.BooleanField(default=False)
    anticipop = models.BooleanField(default=False)
    tiposervicio = models.ForeignKey(Islr, verbose_name="Tipo de servicio", on_delete=models.PROTECT)
    departamento = models.ForeignKey(departamento, verbose_name="Departamento", on_delete=models.PROTECT, null=True, default= None)
    tipo = models.CharField(max_length=3, choices=choise_tipo, default='ser', verbose_name="Tipo de Factura")

    def antiguedad(self):
        return (datetime.now().date() - self.fecharecepcion)

    def caliva(self):
        return self.big * self.iva / 100

    def total(self):
        return self.caliva() + self.big + self.exento

    def calretiva(self):
        return self.caliva() * self.retiva / 100

    def calislr(self):
        return ((self.big + self.exento) * self.islr / 100) - self.sustraendo

    def totalusd(self):
        if self.cambiofactura > 0:
            return self.total() / self.cambiofactura
        else:
            return 0

    def pagousd(self):
        if self.cambiofactura > 0:
            return ((self.total() - self.calretiva() - self.calislr()) - (self.caliva() - self.calretiva())) / self.cambiofactura
        else:
            return 0
    
    def totalbs(self):
        return self.caliva() - self.calretiva()

    def pagoenbs(self):
        if self.cambiopago > 0:
            return ((self.pagousd() - self.divisa) * self.cambiopago) + self.totalbs()
        else:
            return self.total() - self.calretiva() - self.calislr()

class iva(models.Model):
    porcentaje = models.DecimalField(verbose_name='IVA', max_digits=20, decimal_places=5)

    def __str__(self):
        return self.porcentaje

class anticipo(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT) 
    factura = models.ForeignKey(factura, verbose_name="Factura", on_delete=models.PROTECT, related_name="get_anticipo", null=True, blank=True)
    empresa = models.ForeignKey(Empresa, verbose_name="Proveedor", on_delete=models.PROTECT, related_name="get_anticipo")
    fechapago = models.DateField(verbose_name='Fecha de Pago', null=True,  blank=True)
    montobs = models.DecimalField(verbose_name='BS', max_digits=20, decimal_places=5, default=0)
    montousd = models.DecimalField(verbose_name='USD', max_digits=20, decimal_places=5, default=0)
    estatus = models.BooleanField(default=False)