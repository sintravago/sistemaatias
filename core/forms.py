from django import forms
from .models import visitantes, permisos, extras, guardia
from registration.models import Trabajador

class MarcarForm(forms.Form):
    barcode = forms.IntegerField(label="Código de barra", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Código de barra'}))

class VisitarntesForm(forms.ModelForm):
    class Meta:
        model = visitantes
        fields = ['cedula','nombre','apellido','observacion','departamento','user']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del visitante'}),
            'apellido': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido del visitante'}),
            'cedula': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Ingrese su cédula', 'min':'5'}),
            'observacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas...', 'rows':'3'}),
            'departamento': forms.Select(attrs={'class':'form-control'}),
        }

class PermisosForm(forms.ModelForm):
    class Meta:
        model = permisos
        fields = ['desde','hasta','motivo','observacion','trabajador','archivo','user']
        widgets = {
            'observacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas...', 'rows':'3'}),
            'motivo': forms.Select(attrs={'class':'form-control'}),
        }


class GuardiaForm(forms.ModelForm):
    class Meta:
        model = guardia
        fields = ['entrada','salida','observacion','trabajador','user']
        widgets = {
            'observacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas...', 'rows':'3'}),
            'entrada': forms.TextInput(attrs={'class':'form-control datetimepicker-input', 'data-target':"#reservationdate"})
        }

class ExtrasForm(forms.ModelForm):
    class Meta:
        model = extras
        fields = ['entrada','salida','observacion','trabajador','user']
        widgets = {
            'observacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas...', 'rows':'3'}),
            'entrada': forms.TextInput(attrs={'class':'form-control datetimepicker-input', 'data-target':"#reservationdate"})
        }

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['cedula','codigo','nombre','apellido','sexo','departamento','cargo','nacimiento','tlf1','tlf2','horario']
        widgets = {
            'tlf1': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese su número tlf', 'data-inputmask':"'mask': '(9999) 999-9999'", 'data-mask':'data-mask'}),
            'tlf2': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese su número tlf', 'data-inputmask':"'mask': '(9999) 999-9999'", 'data-mask':'data-mask'})
        }