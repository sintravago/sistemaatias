from django.contrib import admin
from .models import guardia, marca, permisos, visitantes, extras, Supervisor
# Register your models here.

class permisosAdmin(admin.ModelAdmin):
    list_display = ('desde','hasta','trabajador','motivo')

class marcaAdmin(admin.ModelAdmin):
    list_display = ('fecha','tipo','trabajador')

class guardiaAdmin(admin.ModelAdmin):
    list_display = ('trabajador','entrada','salida')

class extrasAdmin(admin.ModelAdmin):
    list_display = ('trabajador','entrada','salida')

class visitantesAdmin(admin.ModelAdmin):
    list_display = ('fecha','tipo','cedula', 'nombre')

class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('user','departamento')

admin.site.register(guardia, guardiaAdmin)
admin.site.register(marca, marcaAdmin)
admin.site.register(permisos, permisosAdmin)
admin.site.register(visitantes, visitantesAdmin)
admin.site.register(extras, extrasAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
