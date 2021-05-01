from django import forms
from .models import factura, Empresa, iva

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['user','rif','rift','razon','clasificacion','direccion','tlf']
        widgets = {
            'rift': forms.Select(attrs={'class':'custom-select', 'style':'width: 100%;'}),
            'rif': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'RIF', 'min':'1'}),
            'razon': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Razón'}),
            'clasificacion': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'direccion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Dirección...', 'rows':'3'}),
            'tlf': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Teléfono', 'data-inputmask':"'mask': '(9999) 999-9999'", 'data-mask':'data-mask'})
        }

class FacturaForm(forms.ModelForm):
    class Meta:
        model = factura
        fields = ['empresa','user','nfactura','ncontrol','fechafactura', 'fecharecepcion', 'concepto', 'big', 'exento', 'archivo', 'cambiofactura', 'cambiopago', 'retiva', 'tiposervicio','divisa']
        widgets = {
            'nfactura': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Número de factura'}),
            'ncontrol': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Número de control', 'min':'1'}),
            'fechafactura': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Factura', 'data-target':'#reservationdate'}),
            'fecharecepcion': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Recepción', 'data-target':'#reservationdate2'}),
            'concepto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Concepto'}),
            'big': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'BIG', 'step':'.01', 'min':'0'}),
            'exento': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Exento', 'step':'.01', 'min':'0'}),
            'cambiofactura': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cambio Factura', 'step':'.01', 'min':'0'}),
            'cambiopago': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cambio Pago', 'step':'.01', 'min':'0'}),
            'archivo': forms.FileInput(attrs={'class':'custom-file-input'}),
            'empresa': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'retiva': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'tiposervicio': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'divisa': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Pago en USD', 'step':'.01', 'min':'0'}),
        }

class FacturaUpdateForm(forms.ModelForm):
    class Meta:
        model = factura
        fields = ['empresa','user','nfactura','ncontrol','fechafactura', 'fecharecepcion', 'concepto', 'big', 'exento', 'archivo']
        widgets = {
            'nfactura': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Número de factura', 'min':'1'}),
            'ncontrol': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Número de control', 'min':'1'}),
            'fechafactura': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Factura', 'data-target':'#reservationdate'}),
            'fecharecepcion': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Recepción', 'data-target':'#reservationdate2'}),
            'concepto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Concepto'}),
            'big': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'BIG', 'step':'.01', 'min':'0'}),
            'exento': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Exento', 'step':'.01', 'min':'0'}),
            'empresa': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
        }

class ivaUpdateForm(forms.ModelForm):
    class Meta:
        model = iva
        fields = ['porcentaje',]
        widgets = {
            'porcentaje': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'IVA', 'step':'.01', 'min':'0'}),
        }