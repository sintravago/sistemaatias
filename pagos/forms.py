from django import forms
from .models import factura

class FacturaForm(forms.Form):
    class Meta:
        model = factura
        fields = ['rif','razon','nfactura','ncontrol','fechafactura']