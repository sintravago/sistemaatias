from django import forms
from .models import factura, Empresa, iva, anticipo

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['user','rif','rift','razon','clasificacion','direccion','tlf', 'retiva']
        widgets = {
            'rift': forms.Select(attrs={'class':'custom-select', 'style':'width: 100%;'}),
            'rif': forms.TextInput(attrs={'class':'form-control', 'placeholder':'RIF'}),
            'razon': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Razón'}),
            'clasificacion': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'retiva': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'direccion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Dirección...', 'rows':'3'}),
            'tlf': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Teléfono', 'data-inputmask':"'mask': '(9999) 999-9999'", 'data-mask':'data-mask'})
        }

class FacturaForm(forms.ModelForm):
    class Meta:
        model = factura
        fields = ['empresa','user','nfactura','ncontrol','fechafactura', 'fecharecepcion', 'concepto', 'big', 'exento', 'archivo', 'cambiofactura', 'cambiopago', 'tiposervicio','divisa', 'retiva', 'departamento', 'tipo']
        widgets = {
            'nfactura': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Número de factura'}),
            'ncontrol': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Número de control'}),
            'fechafactura': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Factura', 'data-target':'#reservationdate'}),
            'fecharecepcion': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Recepción', 'data-target':'#reservationdate2'}),
            'concepto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Concepto'}),
            'big': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'BIG', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'exento': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Exento', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'cambiofactura': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cambio Factura', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'cambiopago': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cambio Pago', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'archivo': forms.FileInput(attrs={'class':'custom-file-input'}),
            'empresa': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'tiposervicio': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'divisa': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Pago en USD', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'departamento': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'tipo': forms.Select(attrs={'class':'form-control', 'style':'width: 100%;'}),
        }

    def clean_nfactura(self):
        nrofactura = self.cleaned_data.get("nfactura")
        empresa = self.cleaned_data.get("empresa")
        if factura.objects.filter(empresa=empresa,nfactura=nrofactura).exists():
            raise forms.ValidationError("La Número de factura ya está registrada")
        return nrofactura
    
    def clean_ncontrol(self):
        ncontrol = self.cleaned_data.get("ncontrol")
        empresa = self.cleaned_data.get("empresa")
        if factura.objects.filter(empresa=empresa,ncontrol=ncontrol).exists():
            raise forms.ValidationError("La Número de control ya está registrado")
        return ncontrol

class FacturaEditForm(forms.ModelForm):
    class Meta:
        model = factura
        fields = ['empresa','user','nfactura','ncontrol','fechafactura', 'fecharecepcion', 'concepto', 'big', 'exento', 'archivo', 'cambiofactura', 'cambiopago', 'tiposervicio','divisa', 'retiva', 'departamento','tipo']
        widgets = {
            'nfactura': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Número de factura'}),
            'ncontrol': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Número de control'}),
            'fechafactura': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Factura', 'data-target':'#reservationdate'}),
            'fecharecepcion': forms.DateInput (attrs={'class':'form-control datetimepicker-input', 'placeholder':'Fecha de Recepción', 'data-target':'#reservationdate2'}),
            'concepto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Concepto'}),
            'big': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'BIG', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'exento': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Exento', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'cambiofactura': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cambio Factura', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'cambiopago': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cambio Pago', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'empresa': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'tiposervicio': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'divisa': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Pago en USD', 'step':'.00001', 'min':'0', 'onkeyup':'calculariva()'}),
            'departamento': forms.Select(attrs={'class':'select2bs4', 'style':'width: 100%;'}),
            'tipo': forms.Select(attrs={'class':'form-control', 'style':'width: 100%;'}),
        }

class ivaUpdateForm(forms.ModelForm):
    class Meta:
        model = iva
        fields = ['porcentaje',]
        widgets = {
            'porcentaje': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'IVA', 'step':'.01', 'min':'0'}),
        }

class AnticipoForm(forms.ModelForm):
    class Meta:
        model = anticipo
        fields = ['factura','montobs','montousd', 'cambio','user']
        widgets = {
            'montobs': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Pago en BS', 'step':'.00001', 'min':'0', 'onkeyup':'calculartotal()'}),
            'montousd': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'pago en USD', 'step':'.00001', 'min':'0', 'onkeyup':'calculartotal()'}),
            'cambio': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'pago en USD', 'step':'.00001', 'min':'0', 'onkeyup':'calculartotal()'}),
        }
