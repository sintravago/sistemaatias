from .forms import EmailForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms


# Create your views here.


@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('registration:email_done')
    template_name = 'registration/email_form.html'

    def get_object(self):
        # recuperar el objeto que se va editar
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Email'})
        return form
    
@method_decorator(login_required, name='dispatch')
class EmailDoneView(TemplateView):
    template_name = "registration/email_done.html"



