from django.contrib import admin
from .models import factura
# Register your models here.

class facturaAdmin(admin.ModelAdmin):
    list_display = ('rif','razon','big')

admin.site.register(factura, facturaAdmin)
