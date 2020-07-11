from django.contrib import admin
from .models import Trabajador, horas
# Register your models here.

class TrabajadorAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('codigo','cedula','nombre','apellido','cargo','departamento','entrada','salida')

class horasAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'fecha', 'entrada', 'salida')

admin.site.register(Trabajador, TrabajadorAdmin)
admin.site.register(horas, horasAdmin)
