from django import forms
from django.contrib.auth.models import User


class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True,label="Email", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Ingrese sus email'}))

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email