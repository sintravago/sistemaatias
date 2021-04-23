from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import FacturaForm, FacturaUpdateForm
from .models import factura
from django.db.models import Q

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
        object_list = self.model.objects.filter(estatus__in = ("R","S"))
        if "search" in self.request.GET:
            name = self.request.GET['search']
            if (name != ''):
                if len(name.split()) > 1:
                    for x in name.split():
                        object_list = object_list.filter(Q(razon__icontains = x) | Q(gerencia__nombre__icontains = x))
                else:
                    object_list = object_list.filter(Q(razon__icontains = name) | Q(concepto__icontains = name) | Q(rif__icontains = name) | Q(monto__icontains = name) | Q(iva__icontains = name) | Q(islr__icontains = name) | Q(gerencia__nombre__icontains = name))
        if "estatus" in self.request.GET:
            if self.request.GET["estatus"] != "0" :
                object_list = object_list.filter(estatus = self.request.GET["estatus"])
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estados = (("R", "Registradas"), ("S", "Seleccionadas"))
        context['estados'] = estados
        print(estados)
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
class FacturaSelecListView(ListView):
    model = factura
    template_name = 'pagos/facturas.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = self.model.objects.filter(estatus__in = ("R","S"))
        if "search" in self.request.GET:
            name = self.request.GET['search']
            if (name != ''):
                if len(name.split()) > 1:
                    for x in name.split():
                        object_list = object_list.filter(Q(razon__icontains = x) | Q(gerencia__nombre__icontains = x))
                else:
                    object_list = object_list.filter(Q(razon__icontains = name) | Q(concepto__icontains = name) | Q(rif__icontains = name) | Q(monto__icontains = name) | Q(iva__icontains = name) | Q(islr__icontains = name) | Q(gerencia__nombre__icontains = name))
        if "estatus" in self.request.GET:
            if self.request.GET["estatus"] != "0" :
                object_list = object_list.filter(estatus = self.request.GET["estatus"])
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estados = (("A", "Aprobadas"), ("S", "Seleccionadas"))
        context['estados'] = estados
        print(estados)
        return context



