from django.db import models

# Create your models here.

class Trabajador(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')
    codigo = models.IntegerField(verbose_name='Código', null=True, blank=True)
    nombre = models.CharField(max_length=150 , verbose_name='Nombre')
    apellido = models.CharField(max_length=150 , verbose_name='Apellido')
    cedula = models.IntegerField(verbose_name='Cédula')
    cargo = models.CharField(max_length=150 , verbose_name='Cargo')
    departamento = models.CharField(max_length=150 , verbose_name='Departamento')
    entrada = models.TimeField(verbose_name='entrada')
    salida = models.TimeField(verbose_name='Salida')

    def __str__(self):
        return (self.nombre + ' ' + self.apellido)

    class Meta:
        verbose_name = 'trabajador'
        verbose_name_plural = 'trabajadores'
        ordering = ['codigo']

class horas(models.Model):
    entrada = models.TimeField(auto_now_add=True, verbose_name='Entrada')
    entrada.editable = True
    salida = models.TimeField(verbose_name='Salida', null = True, blank= True)
    fecha = models.DateField(auto_now=True,verbose_name='Fecha')
    fecha.editable = True
    trabajador = models.ForeignKey(Trabajador, verbose_name="Trabajador", on_delete=models.CASCADE)

    def __str__(self):
        if self.salida:
            diferencia = (self.salida.hour * 3600 + self.salida.minute * 60 + self.salida.second) - (self.entrada.hour * 3600 + self.entrada.minute * 60 + self.entrada.second)
            minutos = int(diferencia / 60)
            segundos = int(diferencia % 60)
            horas = int(minutos / 60)
            minutos = int(minutos % 60)
            return str(horas) + ':' + str(minutos) + ':' + str(segundos)
        else:
            return str(0)

    class Meta:
        verbose_name = 'Horas'
        verbose_name_plural = 'Horas'
        ordering = ['fecha']