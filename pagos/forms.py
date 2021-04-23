from django import forms
from .models import factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = factura
        fields = ['rif','razon','nfactura','ncontrol','fechafactura', 'fecharecepcion', 'concepto', 'monto', 'iva', 'islr', 'gerencia', 'direccion', 'archivo']
        labels = {
            'rif': 'RIF',
        }
        widgets = {
            'rif': forms.TextInput(attrs={'class':'form-control', 'placeholder':'RIF'}),
            'razon': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Razón Social'}),
            'nfactura': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Número de factura', 'min':'1'}),
            'ncontrol': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Número de control', 'min':'1'}),
            'fechafactura': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Factura', 'data-target':'#reservationdate'}),
            'fecharecepcion': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Recepción', 'data-target':'#reservationdate2'}),
            'concepto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Concepto'}),
            'monto': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Monto', 'step':'.01', 'min':'0'}),
            'iva': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'IVA', 'step':'.01', 'min':'0'}),
            'islr': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'ISLR', 'step':'.01', 'min':'0'}),
            'gerencia': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'direccion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Dirección Corporativa', 'rows':'3'}),
            'archivo': forms.FileInput(attrs={'class':'custom-file-input'}),
        }

class FacturaUpdateForm(forms.ModelForm):
    class Meta:
        model = factura
        fields = ['estatus','rif','razon','nfactura','ncontrol','fechafactura', 'fecharecepcion', 'concepto', 'monto', 'iva', 'islr', 'gerencia', 'direccion', 'archivo']
        labels = {
            'rif': 'RIF',
        }
        widgets = {
            'rif': forms.TextInput(attrs={'class':'form-control', 'placeholder':'RIF'}),
            'razon': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Razón Social'}),
            'nfactura': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Número de factura', 'min':'1'}),
            'ncontrol': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Número de control', 'min':'1'}),
            'fechafactura': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Factura', 'data-target':'#reservationdate'}),
            'fecharecepcion': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Recepción', 'data-target':'#reservationdate2'}),
            'concepto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Concepto'}),
            'monto': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Monto', 'step':'.01', 'min':'0'}),
            'iva': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'IVA', 'step':'.01', 'min':'0'}),
            'islr': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'ISLR', 'step':'.01', 'min':'0'}),
            'gerencia': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'direccion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Dirección Corporativa', 'rows':'3'}), 
            'estatus': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
        }

class FacturaUpdatestatusForm(forms.ModelForm):
    class Meta:
        model = factura
        fields = ['estatus',]
        labels = {
            'estatus': 'Estatus',
        }
        widgets = {
            'estatus': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
        }