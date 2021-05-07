from django.contrib import admin
from .models import factura, Islr
# Register your models here.

class facturaAdmin(admin.ModelAdmin):
    list_display = ('empresa','big','exento')

class IslrAdmin(admin.ModelAdmin):
    list_display = ('codigo','actividad','porcentaje','sustraendo')

admin.site.register(factura, facturaAdmin)
admin.site.register(Islr, IslrAdmin)
