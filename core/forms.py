from django import forms

class MarcarForm(forms.Form):
    barcode = forms.IntegerField(label="Código de barra", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Código de barra'}))
