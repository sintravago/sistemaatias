from django.db import models
from django.contrib.auth.models import User

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
    desde = models.DateTimeField()
    hasta = models.DateTimeField()
    motivo = models.CharField(max_length=1, choices=tipo_permiso, default='P',)
    observacion = models.TextField(verbose_name="Observaciones", blank=True, null=True)
    trabajador = models.ForeignKey(User, verbose_name="Trabajador", on_delete=models.CASCADE, related_name="get_trabajador")
    archivo = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE, related_name="get_usuario")

class guardia(models.Model):
    entrada = models.TimeField()
    salida = models.TimeField()
    fecha = models.DateField()
    trabajador = models.ForeignKey(User, verbose_name="Trabajador", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.fecha

class marca(models.Model):
    tipo_marca = [
        ('E', 'Entrada'),
        ('S', 'Salida'),
    ]
    modo_marca = [
        (1, 'Regular'),
        (2, 'Guardia'),
    ]
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='fecha')
    tipo = models.CharField(max_length=1, choices=tipo_marca, default='E')
    modo = models.CharField(max_length=1, choices=tipo_marca, default=1)
    trabajador = models.ForeignKey(User, verbose_name="Trabajador", on_delete=models.CASCADE)

    def __str__(self):
        return "{:%d/%m/%Y}".format(self.fecha)

    class Meta:
        ordering = ['-pk']