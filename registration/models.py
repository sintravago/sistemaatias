from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime

class cargo(models.Model):
	contrato = models.CharField(max_length=150 , verbose_name='contrato')
	consecutivo = models.IntegerField(verbose_name='consecutivo')
	nombre = models.CharField(max_length=150 , verbose_name='Nombre')
	
	def __str__(self):
		return self.nombre
		
class departamento(models.Model):
    nombre = models.CharField(max_length=150 , verbose_name='Nombre')

    def __str__(self):
        return self.nombre

class dia(models.Model):
    nombre = models.CharField(max_length=50 , verbose_name='Nombre')

    def __str__(self):
        return self.nombre

class horario(models.Model):
    nombre = models.CharField(max_length=150 , verbose_name='Nombre')
    dias = models.ManyToManyField(dia)
    entrada = models.TimeField()
    salida = models.TimeField()

    def __str__(self):
        return self.nombre

class Trabajador(models.Model):
    sexo_select = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    choise_estatus = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]
	
    nombre = models.CharField(max_length=100 , verbose_name='Nombre')
    apellido = models.CharField(max_length=100 , verbose_name='Apellido')
    codigo = models.IntegerField(verbose_name='Código', null=True, blank=True)
    cedula = models.IntegerField(verbose_name='Cédula')
    cargo = models.ForeignKey(cargo, verbose_name="Cargo", on_delete=models.CASCADE)
    departamento = models.ForeignKey(departamento, verbose_name="Departamento", on_delete=models.CASCADE)
    nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=sexo_select, default='M',)
    tlf1 = models.CharField(max_length=50 , verbose_name='Teléfono 1', null = True, blank = True)
    tlf2 = models.CharField(max_length=50 , verbose_name='Teléfono 2', null = True, blank = True)
    horario = models.ForeignKey(horario, verbose_name="Horario", on_delete=models.CASCADE)
    estatus = models.CharField(max_length=1, choices=choise_estatus, default='A',)

    def __str__(self):
        return (self.nombre + ' ' + self.apellido)

    def edad(self):
        return int((datetime.now().date() - self.nacimiento).days / 365.25)

    class Meta:
        verbose_name = 'trabajador'
        verbose_name_plural = 'trabajadores'
        ordering = ['cedula']

#@receiver(post_save, sender=User)
#def ensure_profile_exists(sender, instance, **kwargs):
#    if kwargs.get('created', False):
#        Profile.objects.get_or_create(user=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado")

