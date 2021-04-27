from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import FacturaForm, FacturaUpdateForm, FacturaUpdatestatusForm
from .models import factura
from django.db.models import Q, Sum, F
from django.contrib.auth.models import User, Group

# Create your views here.
@method_decorator(login_required, name='dispatch')
class FacturaCreateView(CreateView):
    form_class = FacturaForm
    template_name = 'pagos/factura_add.html'
    success_url = reverse_lazy("pagos:factura_add")

@method_decorator(login_required, name='dispatch')
class FacturaListView(ListView):
    model = factura
    template_name = 'pagos/facturas.html'
    paginate_by = 10

    def get_queryset(self):
        grupo1 = Group.objects.get(name="nivel1")
        grupo2 = Group.objects.get(name="nivel2")
        grupo3 = Group.objects.get(name="nivel3")
        object_list = self.model.objects.none()
        if grupo1 in self.request.user.groups.all():
            object_list = self.model.objects.filter(estatus2 = False).annotate(suma=Sum(F('monto') + F('iva') + F('islr')))
        elif grupo2 in self.request.user.groups.all():
            object_list = self.model.objects.filter(estatus2 = False).annotate(suma=Sum(F('monto') + F('iva') + F('islr')))
        elif grupo3 in self.request.user.groups.all():
            object_list = self.model.objects.filter(estatus = True).annotate(suma=Sum(F('monto') + F('iva') + F('islr')))
        if "search" in self.request.GET:
            name = self.request.GET['search']
            if (name != ''):
                if len(name.split()) > 1:
                    for x in name.split():
                        object_list = object_list.filter(Q(razon__icontains = x) | Q(gerencia__nombre__icontains = x))
                else:
                    object_list = object_list.filter(Q(razon__icontains = name) | Q(concepto__icontains = name) | Q(rif__icontains = name) | Q(suma__icontains = name) | Q(gerencia__nombre__icontains = name))
        if "estatus" in self.request.GET:
            if self.request.GET["estatus"] != "0" :
                object_list = object_list.filter(estatus = self.request.GET["estatus"])
        if "ord" in self.request.GET:
            if self.request.GET["ord"] == "asc" :
                object_list = object_list.order_by("fecharecepcion")
            else:
                object_list = object_list.order_by("-fecharecepcion")
        else:
            object_list = object_list.order_by("-fecharecepcion")

        if "actu" in self.request.GET:
            actualizar = factura.objects.get(pk = self.request.GET["actu"])
            if actualizar.estatus == True:
                actualizar.estatus = False
            else:
                actualizar.estatus = True
            actualizar.save()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo1 = Group.objects.get(name="nivel1")
        grupo2 = Group.objects.get(name="nivel2")
        grupo3 = Group.objects.get(name="nivel3")
        estados = (("",""),("",""))
        if grupo1 in self.request.user.groups.all():
            estados = (("R", "Registradas"), ("S", "Seleccionadas"))
        elif grupo2 in self.request.user.groups.all():
            estados = (("S", "Seleccionadas"), ("A", "Aprobadas"))
        elif grupo3 in self.request.user.groups.all():
            estados = (("A", "Aprobadas"), ("P", "Pagadas"))
        
        context['estados'] = estados
        return context

@method_decorator(login_required, name='dispatch')
class FacturaDetailView(DetailView):
    model = factura
    template_name = 'pagos/factura_view.html'

@method_decorator(login_required, name='dispatch')
class FacturaUpdate(UpdateView):
    form_class = FacturaUpdateForm
    model = factura
    template_name = 'pagos/factura_edit.html'

    def get_success_url(self):
        return reverse_lazy("pagos:factura_view", kwargs={'pk': self.kwargs['pk']})

@method_decorator(login_required, name='dispatch')
class FacturaUpdatestatus(UpdateView):
    form_class = FacturaUpdatestatusForm
    model = factura
    template_name = 'pagos/factura_edit_status.html'

    def get_success_url(self):
        return reverse_lazy("pagos:factura_view", kwargs={'pk': self.kwargs['pk']})

class ReporteView(TemplateView):

    template_name = "pagos/reporte.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        select = factura.objects.filter(estatus = "S")
        reg = factura.objects.filter(estatus = "R")
        apro = factura.objects.filter(estatus = "A")
        paga = factura.objects.filter(estatus = "P")
        if select.count() > 0:
            context['selectm'] = select.aggregate(suma=Sum(F('monto') + F('iva') + F('islr')))['suma']
            context['selectc'] = select.count()
        if reg.count() > 0:
            context['regm'] = reg.aggregate(suma=Sum(F('monto') + F('iva') + F('islr')))['suma']
            context['regc'] = reg.count()
        if apro.count() > 0:
            context['aprom'] = apro.aggregate(suma=Sum(F('monto') + F('iva') + F('islr')))['suma']
            context['aproc'] = apro.count()
        if paga.count() > 0:
            context['pagam'] = paga.aggregate(suma=Sum(F('monto') + F('iva') + F('islr')))['suma']
            context['pagac'] = paga.count()
        return context