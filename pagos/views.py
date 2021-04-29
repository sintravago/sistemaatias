from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import FacturaForm, FacturaUpdateForm
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
            object_list = self.model.objects.filter(estatus2 = False).annotate(suma=Sum(F('big') + F('iva') + F('excento')))
        elif grupo2 in self.request.user.groups.all():
            object_list = self.model.objects.filter(estatus2 = False).annotate(suma=Sum(F('big') + F('iva') + F('excento')))
        elif grupo3 in self.request.user.groups.all():
            object_list = self.model.objects.filter(estatus = True).annotate(suma=Sum(F('big') + F('iva') + F('excento')))
        if "search" in self.request.GET:
            name = self.request.GET['search']
            if (name != ''):
                if len(name.split()) > 1:
                    for x in name.split():
                        object_list = object_list.filter(Q(razon__icontains = x) | Q(gerencia__nombre__icontains = x))
                else:
                    object_list = object_list.filter(Q(razon__icontains = name) | Q(rif__icontains = name) | Q(suma__icontains = name) | Q(gerencia__nombre__icontains = name))
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
    form_class = FacturaUpdateForm
    model = factura
    template_name = 'pagos/factura_edit.html'

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
            context['selectm'] = select.aggregate(suma=Sum(F('big') + F('iva') + F('excento')))['suma']
            context['selectc'] = select.count()
        if reg.count() > 0:
            context['regm'] = reg.aggregate(suma=Sum(F('big') + F('iva') + F('excento')))['suma']
            context['regc'] = reg.count()
        if apro.count() > 0:
            context['aprom'] = apro.aggregate(suma=Sum(F('big') + F('iva') + F('excento')))['suma']
            context['aproc'] = apro.count()
        if paga.count() > 0:
            context['pagam'] = paga.aggregate(suma=Sum(F('big') + F('iva') + F('excento')))['suma']
            context['pagac'] = paga.count()
        return context