from django import forms
from .models import visitantes, permisos, extras

class MarcarForm(forms.Form):
    barcode = forms.IntegerField(label="Código de barra", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Código de barra'}))

class VisitarntesForm(forms.ModelForm):
    class Meta:
        model = visitantes
        fields = ['cedula','nombre','apellido','observacion','departamento','tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del visitante'}),
            'apellido': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido del visitante'}),
            'cedula': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Ingrese su cédula', 'min':'5'}),
            'observacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas...', 'rows':'3'}),
            'departamento': forms.Select(attrs={'class':'form-control'}),
            'tipo': forms.RadioSelect(),
        }

class PermisosForm(forms.ModelForm):
    class Meta:
        model = permisos
        fields = ['desde','hasta','motivo','observacion','trabajador','archivo','user']
        widgets = {
            'observacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas...', 'rows':'3'}),
            'motivo': forms.Select(attrs={'class':'form-control'}),
        }


class ExtrasForm(forms.ModelForm):
    class Meta:
        model = extras
        fields = ['entrada','salida','observacion','trabajador','user']
        widgets = {
            'observacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas...', 'rows':'3'}),
        }