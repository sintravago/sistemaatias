from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import FacturaForm, FacturaUpdateForm, EmpresaForm, ivaUpdateForm
from .models import factura, Empresa, iva, Islr
from django.db.models import Q, Sum, F
from django.contrib.auth.models import User, Group
from django.http import JsonResponse

# Create your views here.

@method_decorator(login_required, name='dispatch')
class EmpresaCreateView(CreateView):
    form_class = EmpresaForm
    template_name = 'pagos/empresa_add.html'
    success_url = reverse_lazy("pagos:empresas")

@method_decorator(login_required, name='dispatch')
class EmpresaListView(ListView):
    model = Empresa
    template_name = 'pagos/empresas.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = self.model.objects.all()
        if "search" in self.request.GET:
            name = self.request.GET['search']
            if (name != ''):
                if len(name.split()) > 1:
                    for x in name.split():
                        object_list = object_list.filter(razon__icontains = x)
                else:
                    object_list = object_list.filter(Q(razon__icontains = name) | Q(rif__icontains = name))
        return object_list

@method_decorator(login_required, name='dispatch')
class EmpresaUpdate(UpdateView):
    form_class = EmpresaForm
    model = Empresa
    template_name = 'pagos/empresa_edit.html'

    def get_success_url(self):
        return reverse_lazy("pagos:empresas")

@method_decorator(login_required, name='dispatch')
class FacturaCreateView(CreateView):
    form_class = FacturaForm
    template_name = 'pagos/factura_add.html'
    success_url = reverse_lazy("pagos:factura_add")

    def get_success_url(self):
        self.object.iva = iva.objects.get(id=1).porcentaje
        self.object.islr = self.object.tiposervicio.porcentaje
        self.object.save()
        return reverse_lazy("pagos:factura_view", kwargs={'pk': self.kwargs['pk']})

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
            object_list = self.model.objects.filter(estatus2 = False).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
        elif grupo2 in self.request.user.groups.all():
            object_list = self.model.objects.filter(estatus2 = False).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
        elif grupo3 in self.request.user.groups.all():
            object_list = self.model.objects.filter(estatus = True).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
        if "search" in self.request.GET:
            name = self.request.GET['search']
            if (name != ''):
                if len(name.split()) > 1:
                    for x in name.split():
                        object_list = object_list.filter(empresa__razon__icontains = x)
                else:
                    object_list = object_list.filter(Q(empresa__razon__icontains = name) | Q(empresa__rif__icontains = name) | Q(suma__icontains = name) )
        if "estatus" in self.request.GET:
            if self.request.GET["estatus"] != "0" :
                if grupo3 in self.request.user.groups.all():
                    object_list = object_list.filter(estatus2 = self.request.GET["estatus"])
                else:
                    object_list = object_list.filter(estatus = self.request.GET["estatus"])
        if "ord" in self.request.GET:
            if self.request.GET["ord"] == "asc" :
                object_list = object_list.order_by("fecharecepcion")
            else:
                object_list = object_list.order_by("-fecharecepcion")
        else:
            object_list = object_list.order_by("-fecharecepcion")
            
        return object_list

def facturaStatusUpdate(request,pk):
    actualizar = factura.objects.get(pk = pk)
    if actualizar.estatus == True:
        actualizar.estatus = False
    else:
        actualizar.estatus = True
    actualizar.save()
    add = "?suc=1"
    if "search" in request.GET:
        add += "&search=" + request.GET["search"]
    if "ord" in request.GET:
        add += "&ord=" + request.GET["ord"]
    if "page" in request.GET:
        add += "&page=" + request.GET["page"]
    if "estatus" in request.GET:
        add += "&estatus=" + request.GET["estatus"]
    return redirect(reverse("pagos:facturas")+add)

def facturaStatusUpdate2(request,pk):
    actualizar = factura.objects.get(pk = pk)
    if actualizar.estatus2 == True:
        actualizar.estatus2 = False
    else:
        actualizar.estatus2 = True
    actualizar.save()
    add = "?suc=1"
    if "search" in request.GET:
        add += "&search=" + request.GET["search"]
    if "ord" in request.GET:
        add += "&ord=" + request.GET["ord"]
    if "page" in request.GET:
        add += "&page=" + request.GET["page"]
    if "estatus" in request.GET:
        add += "&estatus=" + request.GET["estatus"]
    return redirect(reverse("pagos:facturas")+add)

@method_decorator(login_required, name='dispatch')
class FacturaDetailView(DetailView):
    model = factura
    template_name = 'pagos/factura_view.html'

@method_decorator(login_required, name='dispatch')
class FacturaUpdate(UpdateView):
    form_class = FacturaForm
    template_name = 'pagos/factura_add.html'
    model = factura

    def get_success_url(self):
        self.object.iva = iva.objects.get(id=1).porcentaje
        self.object.islr = self.object.tiposervicio.porcentaje
        self.object.save()
        return reverse_lazy("pagos:factura_view", kwargs={'pk': self.kwargs['pk']})
	
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios = Islr.objects.filter(Tipo = self.object.empresa.clasificacion)
        context['servicios'] = servicios
        return context

@method_decorator(login_required, name='dispatch')
class IvaUpdate(UpdateView):
    form_class = ivaUpdateForm
    model = iva
    template_name = 'pagos/iva_edit.html'

    def get_success_url(self):
        return reverse_lazy("pagos:iva_edit", kwargs={'pk': self.kwargs['pk']})

class ReporteView(TemplateView):

    template_name = "pagos/reporte.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        select = factura.objects.filter(estatus = "S")
        reg = factura.objects.filter(estatus = "R")
        apro = factura.objects.filter(estatus = "A")
        paga = factura.objects.filter(estatus = "P")
        if select.count() > 0:
            context['selectm'] = select.aggregate(suma=Sum(F('big') + F('iva') + F('exento')))['suma']
            context['selectc'] = select.count()
        if reg.count() > 0:
            context['regm'] = reg.aggregate(suma=Sum(F('big') + F('iva') + F('exento')))['suma']
            context['regc'] = reg.count()
        if apro.count() > 0:
            context['aprom'] = apro.aggregate(suma=Sum(F('big') + F('iva') + F('exento')))['suma']
            context['aproc'] = apro.count()
        if paga.count() > 0:
            context['pagam'] = paga.aggregate(suma=Sum(F('big') + F('iva') + F('exento')))['suma']
            context['pagac'] = paga.count()
        return context

def get_servicio_ajax(request):
    if request.method == "POST":
        empresa_id = request.POST['empresa_id']
        try:
            emp = Empresa.objects.get(id = empresa_id)
            servicio = Islr.objects.filter(Tipo = emp.clasificacion)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(servicio.values('id', 'codigo')), safe = False)