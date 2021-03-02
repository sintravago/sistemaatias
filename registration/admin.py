from django.contrib import admin
from .models import Trabajador, horario, dia, departamento

class departamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

class diaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('codigo','cedula','cargo','departamento','horario')

class horarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'entrada', 'salida')

admin.site.register(dia, diaAdmin)
admin.site.register(Trabajador, TrabajadorAdmin)
admin.site.register(horario, horarioAdmin)
admin.site.register(departamento, departamentoAdmin)
