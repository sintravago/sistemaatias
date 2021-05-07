from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import FacturaForm, EmpresaForm, ivaUpdateForm, FacturaEditForm, AnticipoForm
from .models import factura, Empresa, iva, Islr, anticipo
from registration.models import departamento
from django.db.models import Q, Sum, F
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from easy_pdf.views import PDFTemplateView
from django.conf import settings
from datetime import datetime
import django_excel as excel

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['iva'] = str(iva.objects.get(id=1).porcentaje).replace(',', '.')
        return context

    def get_success_url(self):
        self.object.iva = iva.objects.get(id=1).porcentaje
        self.object.islr = self.object.tiposervicio.porcentaje
        self.object.sustraendo = self.object.tiposervicio.sustraendo
        self.object.save()
        return reverse_lazy("pagos:factura_view", kwargs={'pk': self.object.id})

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
            object_list = self.model.objects.filter(estatus = True, estatus2 = False, estatus3 = False).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
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
        
        if "departamento" in self.request.GET:
            if self.request.GET["departamento"] != "0":
                object_list = object_list.filter(departamento__id = self.request.GET["departamento"] )

        if "ord" in self.request.GET:
            if self.request.GET["ord"] == "asc" :
                object_list = object_list.order_by("fecharecepcion")
            else:
                object_list = object_list.order_by("-fecharecepcion")
        else:
            object_list = object_list.order_by("-fecharecepcion")
        
        if "tipo" in self.request.GET:
            if self.request.GET["tipo"] == "1":
                object_list = object_list.filter(tipo__in = ['alm','dir'] )
            elif self.request.GET["tipo"] != "0":
                object_list = object_list.filter(tipo = self.request.GET["tipo"])
        
        if "reservation" in self.request.GET:
            desde, hasta = self.request.GET["reservation"].split("-")
            desde = desde.replace(' ','')
            hasta = hasta.replace(' ','')
            desde = datetime.strptime(desde, '%d/%m/%Y')
            hasta = datetime.strptime(hasta, '%d/%m/%Y')
            object_list = object_list.filter(fecharecepcion__gte = desde, fecharecepcion__lte = hasta)
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['departamentos'] = departamento.objects.all()
        context['tipos'] = []
        for tipo in factura.choise_tipo:
            context['tipos'].append({'id':tipo[0],'value':tipo[1]})
        totalbs = 0
        totalusd = 0
        pagobs = 0
        pagousd = 0
        for fact in context['object_list']:
            totalbs += fact.total()
            totalusd += fact.totalusd()
            pagobs += fact.pagoenbs()
            pagousd += fact.divisa
        context['totalbs'] = totalbs
        context['totalusd'] = totalusd
        context['pagobs'] = pagobs
        context['pagousd'] = pagousd
        return context

@method_decorator(login_required, name='dispatch')
class FacturaspListView(ListView):
    model = factura
    template_name = 'pagos/facturasp.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = self.model.objects.filter(estatus2 = True, estatus3 = False).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
        if "search" in self.request.GET:
            name = self.request.GET['search']
            if (name != ''):
                if len(name.split()) > 1:
                    for x in name.split():
                        object_list = object_list.filter(empresa__razon__icontains = x)
                else:
                    object_list = object_list.filter(Q(empresa__razon__icontains = name) | Q(empresa__rif__icontains = name) | Q(suma__icontains = name) )
        
        if "departamento" in self.request.GET:
            if self.request.GET["departamento"] != "0":
                object_list = object_list.filter(departamento__id = self.request.GET["departamento"] )

        if "ord" in self.request.GET:
            if self.request.GET["ord"] == "asc" :
                object_list = object_list.order_by("fecharecepcion")
            else:
                object_list = object_list.order_by("-fecharecepcion")
        else:
            object_list = object_list.order_by("-fecharecepcion")

        if "reservation" in self.request.GET:
            desde, hasta = self.request.GET["reservation"].split("-")
            desde = desde.replace(' ','')
            hasta = hasta.replace(' ','')
            desde = datetime.strptime(desde, '%d/%m/%Y')
            hasta = datetime.strptime(hasta, '%d/%m/%Y')
            object_list = object_list.filter(fecharecepcion__gte = desde, fecharecepcion__lte = hasta)
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['departamentos'] = departamento.objects.all()
        context['tipos'] = []
        for tipo in factura.choise_tipo:
            context['tipos'].append({'id':tipo[0],'value':tipo[1]})
        totalbs = 0
        totalusd = 0
        pagobs = 0
        pagousd = 0
        for fact in context['object_list']:
            totalbs += fact.total()
            totalusd += fact.totalusd()
            pagobs += fact.pagoenbs()
            pagousd += fact.divisa
        context['totalbs'] = totalbs
        context['totalusd'] = totalusd
        context['pagobs'] = pagobs
        context['pagousd'] = pagousd
        return context

@method_decorator(login_required, name='dispatch')
class FacturasppListView(ListView):
    model = factura
    template_name = 'pagos/facturaspp.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = self.model.objects.filter(estatus3 = True).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
        if "search" in self.request.GET:
            name = self.request.GET['search']
            if (name != ''):
                if len(name.split()) > 1:
                    for x in name.split():
                        object_list = object_list.filter(empresa__razon__icontains = x)
                else:
                    object_list = object_list.filter(Q(empresa__razon__icontains = name) | Q(empresa__rif__icontains = name) | Q(suma__icontains = name) )
        
        if "departamento" in self.request.GET:
            if self.request.GET["departamento"] != "0":
                object_list = object_list.filter(departamento__id = self.request.GET["departamento"] )

        if "ord" in self.request.GET:
            if self.request.GET["ord"] == "asc" :
                object_list = object_list.order_by("fecharecepcion")
            else:
                object_list = object_list.order_by("-fecharecepcion")
        else:
            object_list = object_list.order_by("-fecharecepcion")

        if "reservation" in self.request.GET:
            desde, hasta = self.request.GET["reservation"].split("-")
            desde = desde.replace(' ','')
            hasta = hasta.replace(' ','')
            desde = datetime.strptime(desde, '%d/%m/%Y')
            hasta = datetime.strptime(hasta, '%d/%m/%Y')
            object_list = object_list.filter(fechapago__gte = desde, fechapago__lte = hasta)
            
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['departamentos'] = departamento.objects.all()
        context['tipos'] = []
        for tipo in factura.choise_tipo:
            context['tipos'].append({'id':tipo[0],'value':tipo[1]})
        totalbs = 0
        totalusd = 0
        pagobs = 0
        pagousd = 0
        for fact in context['object_list']:
            totalbs += fact.total()
            totalusd += fact.totalusd()
            pagobs += fact.pagoenbs()
            pagousd += fact.divisa
        context['totalbs'] = totalbs
        context['totalusd'] = totalusd
        context['pagobs'] = pagobs
        context['pagousd'] = pagousd
        return context

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
    if "departamento" in request.GET:
        add += "&departamento=" + request.GET["departamento"]
    if "tipo" in request.GET:
        add += "&tipo=" + request.GET["tipo"]    
    
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
    if "departamento" in request.GET:
        add += "&departamento=" + request.GET["departamento"]
    if "tipo" in request.GET:
        add += "&tipo=" + request.GET["tipo"]

    if request.GET["suc"] == "1":
        return redirect(reverse("pagos:facturasp")+add)
    else:
        return redirect(reverse("pagos:facturas")+add)

def facturaStatusUpdate3(request,pk):
    actualizar = factura.objects.get(pk = pk)
    if actualizar.estatus3 == False:
        today    = datetime.now()
        strToday = today.strftime("%Y-%m-%d")
        actualizar.estatus3 = True
        actualizar.fechapago = strToday
        actualizar.save()
    add = "?suc=1"
    if "search" in request.GET:
        add += "&search=" + request.GET["search"]
    if "ord" in request.GET:
        add += "&ord=" + request.GET["ord"]
    if "page" in request.GET:
        add += "&page=" + request.GET["page"]
    if "departamento" in request.GET:
        add += "&departamento=" + request.GET["departamento"]
    if "tipo" in request.GET:
        add += "&tipo=" + request.GET["tipo"]
    return redirect(reverse("pagos:facturasp")+add)

@method_decorator(login_required, name='dispatch')
class FacturaDetailView(DetailView):
    model = factura
    template_name = 'pagos/factura_view.html'

@method_decorator(login_required, name='dispatch')
class FacturaUpdate(UpdateView):
    form_class = FacturaEditForm
    template_name = 'pagos/factura_edit.html'
    model = factura

    def get_success_url(self):
        self.object.iva = iva.objects.get(id=1).porcentaje
        self.object.islr = self.object.tiposervicio.porcentaje
        self.object.sustraendo = self.object.tiposervicio.sustraendo
        self.object.save()
        return reverse_lazy("pagos:factura_view", kwargs={'pk': self.kwargs['pk']})
	
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios = Islr.objects.filter(Tipo = self.object.empresa.clasificacion)
        context['servicios'] = servicios
        context['iva'] = str(self.object.iva).replace(',', '.')
        context['retiva'] = str(self.object.retiva).replace(',', '.')
        context['sustraendo'] = str(self.object.sustraendo).replace(',', '.')
        context['islr'] = str(self.object.islr).replace(',', '.')
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
        result = list(servicio.values('id', 'codigo', 'actividad'))
        result.append({'retiva':emp.retiva})
        return JsonResponse(result, safe = False)

def get_islr_ajax(request):
    if request.method == "POST":
        servicio_id = request.POST['servicio_id']
        try:
            servicio = Islr.objects.filter(id = servicio_id)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        result = list(servicio.values('porcentaje', 'sustraendo'))
        return JsonResponse(result, safe = False)

class FacturaPDFView(PDFTemplateView):
    template_name = 'pagos/facturapdf.html'

    base_url = 'file://' + settings.STATIC_ROOT

    def get_context_data(self, **kwargs):
        fact = factura.objects.get(pk=kwargs['pk'])
        return super(FacturaPDFView, self).get_context_data(
            factura = fact,
            pagesize='letter',
            title='Presupuesto',
            **kwargs
        )

@login_required
def exportarfacturas(request):
    export = []
    if request.GET:
        if request.GET["export"] == "1":
            grupo1 = Group.objects.get(name="nivel1")
            grupo2 = Group.objects.get(name="nivel2")
            grupo3 = Group.objects.get(name="nivel3")
            if grupo1 in request.user.groups.all():
                object_list = factura.objects.filter(estatus2 = False).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
            elif grupo2 in request.user.groups.all():
                object_list = factura.objects.filter(estatus2 = False).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
            elif grupo3 in request.user.groups.all():
                object_list = factura.objects.filter(estatus = True, estatus2 = False, estatus3 = False).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
        elif request.GET["export"] == "2":
            object_list = factura.objects.filter(estatus2 = True, estatus3 = False).annotate(suma=Sum(F('big') + F('iva') + F('exento')))
        else:
            object_list = factura.objects.filter(estatus3 = True).annotate(suma=Sum(F('big') + F('iva') + F('exento')))

        if "search" in request.GET:
            name = request.GET['search']
            if (name != ''):
                if len(name.split()) > 1:
                    for x in name.split():
                        object_list = object_list.filter(empresa__razon__icontains = x)
                else:
                    object_list = object_list.filter(Q(empresa__razon__icontains = name) | Q(empresa__rif__icontains = name) | Q(suma__icontains = name) )
        if "estatus" in request.GET:
            if request.GET["estatus"] != "0" :
                if grupo3 in request.user.groups.all():
                    object_list = object_list.filter(estatus2 = self.request.GET["estatus"])
                else:
                    object_list = object_list.filter(estatus = self.request.GET["estatus"])
        
        if "departamento" in request.GET:
            if request.GET["departamento"] != "0":
                object_list = object_list.filter(departamento__id = self.request.GET["departamento"] )

        if "ord" in request.GET:
            if request.GET["ord"] == "asc" :
                object_list = object_list.order_by("fecharecepcion")
            else:
                object_list = object_list.order_by("-fecharecepcion")
        else:
            object_list = object_list.order_by("-fecharecepcion")
        
        if "tipo" in request.GET:
            if request.GET["tipo"] == "1":
                object_list = object_list.filter(tipo__in = ['alm','dir'] )
            elif request.GET["tipo"] != "0":
                object_list = object_list.filter(tipo = self.request.GET["tipo"])
        
        if "reservation" in request.GET:
            desde, hasta = request.GET["reservation"].split("-")
            desde = desde.replace(' ','')
            hasta = hasta.replace(' ','')
            desde = datetime.strptime(desde, '%d/%m/%Y')
            hasta = datetime.strptime(hasta, '%d/%m/%Y')
            object_list = object_list.filter(fecharecepcion__gte = desde, fecharecepcion__lte = hasta)
        
        export.append([
            'RIF',
            'Razón Social',
            'Clasificación',
            'Tlf',
            'Dirección',
            'N° de Factura',
            'N° de Control',
            'Departamento',
            'Fecha de Factura',
            'Fecha de Recepción',
            'Fecha de Pago',
            'Concepto',
            'Tipo de Factura',
            'Tipo de Servicio',
            'Tipo de Cambio (Factura)',
            'Tipo de Cambio (Fecha de Pago)',
            'BIG',
            'Exento',
            'IVA',
            'Total Factura en BS',
            'Total Factura en USD',
            'Retención IVA',
            'Retención ISLR',
            'Pago en BS',
            'Pago en USD',
        ])

        for fact in object_list:
           export.append([
                "{}-{}".format(fact.empresa.rift, fact.empresa.rif),
                fact.empresa.razon,
                fact.empresa.clasificacion,
                fact.empresa.tlf,
                fact.empresa.direccion,
                fact.nfactura,
                fact.ncontrol,
                fact.departamento.nombre,
                fact.fechafactura,
                fact.fecharecepcion,
                fact.fechapago,
                fact.concepto,
                fact.get_tipo_display(),
                "{}: {}".format(fact.tiposervicio.codigo, fact.tiposervicio.actividad),
                fact.cambiofactura,
                fact.cambiopago,
                fact.big,
                fact.exento,
                fact.caliva(),
                fact.total(),
                fact.totalusd(),
                fact.calretiva(),
                fact.calislr(),
                fact.pagoenbs(),
                fact.divisa,
            ]) 
    sheet = excel.pe.Sheet(export)
    return excel.make_response(sheet, "xlsx", file_name="reporte_excel")

@method_decorator(login_required, name='dispatch')
class AnticipoCreateView(CreateView):
    form_class = AnticipoForm
    template_name = 'pagos/anticipo_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = factura.objects.get(pk=self.kwargs['factura'])
        context['cambio'] = str(round(context['object'].cambiopago,2)).replace(',','.')
        return context

    def get_success_url(self):
        fact = factura.objects.get(pk=self.kwargs['factura'])
        fact.anticipo = True
        fact.save()
        return reverse_lazy("pagos:factura_view", kwargs={'pk': self.object.factura.id})

@method_decorator(login_required, name='dispatch')
class AnticipoListView(ListView):
    model = anticipo
    template_name = 'pagos/anticipos.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = self.model.objects.filter(estatus=False)
        return object_list

@method_decorator(login_required, name='dispatch')
class AnticipopListView(ListView):
    model = anticipo
    template_name = 'pagos/anticipos.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = self.model.objects.filter(estatus=True)
        return object_list

def anticipo_update(request,pk):
    actualizar = anticipo.objects.get(pk = pk)
    if actualizar.estatus == False:
        today    = datetime.now()
        strToday = today.strftime("%Y-%m-%d")
        actualizar.estatus = True
        actualizar.fechapago = strToday
        actualizar.save()
        fact = factura.objects.get(pk=actualizar.factura.pk)
        fact.anticipop = True
        fact.save()

        
    add = "?suc=1"
    if "search" in request.GET:
        add += "&search=" + request.GET["search"]
    if "ord" in request.GET:
        add += "&ord=" + request.GET["ord"]
    if "page" in request.GET:
        add += "&page=" + request.GET["page"]
    if "departamento" in request.GET:
        add += "&departamento=" + request.GET["departamento"]
    if "tipo" in request.GET:
        add += "&tipo=" + request.GET["tipo"]
    return redirect(reverse("pagos:anticipos")+add)