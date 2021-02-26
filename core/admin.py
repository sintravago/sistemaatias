from django.contrib import admin
from .models import guardia, marca, permisos
# Register your models here.

class permisosAdmin(admin.ModelAdmin):
    list_display = ('desde','hasta','trabajador','motivo')

class marcaAdmin(admin.ModelAdmin):
    list_display = ('fecha','tipo','modo','trabajador')

class guardiaAdmin(admin.ModelAdmin):
    list_display = ('trabajador','entrada','salida')

admin.site.register(guardia, guardiaAdmin)
admin.site.register(marca, marcaAdmin)
admin.site.register(permisos, permisosAdmin)



