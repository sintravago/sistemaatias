from django.db import models
from django.contrib.auth.models import User
from registration.models import departamento, Trabajador
# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class permisos(models.Model):
    tipo_permiso = [
        ('P', 'Permiso'),
        ('V', 'Vacaciones'),
        ('R', 'Reposo'),
        ('O', 'Otro'),
    ]
    desde = models.DateField()
    hasta = models.DateField()
    motivo = models.CharField(max_length=1, choices=tipo_permiso, default='P',)
    observacion = models.TextField(verbose_name="Observaciones", blank=True, null=True)
    trabajador = models.ForeignKey(Trabajador, verbose_name="Trabajador", on_delete=models.PROTECT, related_name="get_trabajador")
    archivo = models.FileField(upload_to=user_directory_path, null=True,  blank=True)
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT, related_name="get_usuario")

class extras(models.Model):
    entrada = models.DateTimeField()
    salida = models.DateTimeField()
    observacion = models.TextField(verbose_name="Observaciones", blank=True, null=True)
    trabajador = models.ForeignKey(Trabajador, verbose_name="Trabajador", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT, related_name="get_user")
    
    def __str__(self):
        return "{} - {}".format(self.entrada,self.salida)
    
    def diferencia(self):
        dif = (self.salida - self.entrada).total_seconds()
        horas = int(dif // 3600)
        segundos = int(dif % 3600)
        minutos = int(segundos // 60)
        segundo = int(segundos % 60)

        return "{:02d}:{:02d}:{:02d}".format(horas,minutos,segundos)
        

class guardia(models.Model):
    entrada = models.DateTimeField()
    salida = models.DateTimeField()
    observacion = models.TextField(verbose_name="Observaciones", blank=True, null=True)
    trabajador = models.ForeignKey(Trabajador, verbose_name="Trabajador", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT, related_name="get_user_g")
    
    def __str__(self):
        return "{} - {}".format(self.entrada,self.salida)

class marca(models.Model):
    tipo_marca = [
        ('E', 'Entrada'),
        ('S', 'Salida'),
    ]
    modo_marca = [
        ('R', 'Regular'),
        ('G', 'Guardia'),
    ]
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='fecha')
    tipo = models.CharField(max_length=1, choices=tipo_marca, default='E')
    modo = models.CharField(max_length=1, choices=modo_marca, default='R')
    observacion = models.TextField(verbose_name="Observaciones", blank=True, null=True)
    trabajador = models.ForeignKey(Trabajador, verbose_name="Trabajador", on_delete=models.PROTECT)

    def __str__(self):
        return "{:%d/%m/%Y}".format(self.fecha)

    class Meta:
        ordering = ['-pk']

class visitantes(models.Model):
    tipo_marca = [
        ('E', 'Entrada'),
        ('S', 'Salida'),
    ]

    nombre = models.CharField(max_length=100 , verbose_name='Nombre')
    apellido = models.CharField(max_length=100 , verbose_name='Apellido')
    cedula = models.IntegerField(verbose_name='Cédula')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='fecha')
    tipo = models.CharField(max_length=1, verbose_name="Tipo", choices=tipo_marca, default='E')
    observacion = models.TextField(verbose_name="Observaciones", blank=True, null=True)
    departamento = models.ForeignKey(departamento, verbose_name="Departamento", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT, related_name="get_user_v")