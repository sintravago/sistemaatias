from django.shortcuts import render
from .forms import MarcarForm, VisitarntesForm, PermisosForm, ExtrasForm, TrabajadorForm
from registration.models import Trabajador, horario, departamento, cargo, horario
from .models import marca, guardia, permisos, visitantes, extras
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from easy_pdf.views import PDFTemplateView
from django.conf import settings
import django_excel as excel
from datetime import datetime
from django.db.models import Q
# Create your views here.

def marcar(request):
    form = MarcarForm()
    if request.method == 'POST':
        form = MarcarForm(request.POST)
        if form.is_valid():
            if (Trabajador.objects.filter(cedula=form.cleaned_data['barcode']).exists()):
                
                trabajador = Trabajador.objects.get(cedula=form.cleaned_data['barcode'])
                if 'entrada' in request.POST:
                    e = "E"
                else:
                    e = "S"
                if marca.objects.filter(trabajador=trabajador).exists():
                    ultima = marca.objects.filter(trabajador=trabajador).first()
                    if ultima.tipo == e:
                        return render(request,'core/marcar.html',{'form':form, 'marca':'ya', 'e': e})
                elif e == "S":
                    return render(request,'core/marcar.html',{'form':form, 'marca':'p'})
                m = marca(trabajador=trabajador, tipo=e)
                m.save()
                return render(request,'core/marcar.html',{'form':form, 'trabajador':trabajador, 'marca':e, 'hora':m.fecha})
            else:
                return render(request,'core/marcar.html',{'form':form, 'marca':'no'})
    return render(request,'core/marcar.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class TrabajadorCreateView(CreateView):
    form_class = TrabajadorForm
    template_name = 'core/trabajador_add.html'
    success_url = reverse_lazy("core:trabajador_add")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dep = departamento.objects.all()
        sex = Trabajador.sexo_select
        car = cargo.objects.all()
        hor = horario.objects.all()
        context["departamento"] = dep
        context["cargo"] = car
        context["sexo"] = sex
        context["horario"] = hor
        return context

@method_decorator(login_required, name='dispatch')
class TrabajadoresListView(ListView):
    model = Trabajador
    template_name = 'core/trabajadores.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = self.model.objects.all()
        
        if self.request.method == "GET":
            if "search" in self.request.GET:
                name = self.request.GET['search']
                if (name != ''):
                    if len(name.split()) > 1:
                        for x in name.split():
                            object_list = object_list.filter(Q(nombre__icontains = x) | Q(apellido__icontains = x))
                    else:
                        object_list = object_list.filter(Q(nombre__icontains = name) | Q(apellido__icontains = name) | Q(cedula__icontains = name) | Q(cargo__nombre__icontains = name) | Q(departamento__nombre__icontains = name) | Q(codigo__icontains = name))
            if "departamento" in self.request.GET:
                depart = self.request.GET["departamento"]
                if depart != "0":
                    object_list = object_list.filter(departamento__id = depart)

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departamentos'] = departamento.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class TrabajadorDetailView(DetailView):
    model = Trabajador
    template_name = 'core/trabajador_view.html'

@method_decorator(login_required, name='dispatch')
class TrabajadorUpdate(UpdateView):
    form_class = TrabajadorForm
    model = Trabajador
    template_name = 'core/trabajador_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dep = departamento.objects.all()
        sex = Trabajador.sexo_select
        car = cargo.objects.all()
        hor = horario.objects.all()
        context["departamento"] = dep
        context["cargo"] = car
        context["sexo"] = sex
        context["horario"] = hor
        return context
    
    def get_success_url(self):
        return reverse_lazy("core:trabajador_view", kwargs={'pk': self.kwargs['pk']})

@method_decorator(login_required, name='dispatch')
class PermisosCreateView(CreateView):
    form_class = PermisosForm
    template_name = 'core/permiso_add.html'
    success_url = reverse_lazy("core:permiso_add")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        per = permisos.tipo_permiso
        tra = Trabajador.objects.all()
        context["tipo_permiso"] = per
        context["trabajadores"] = tra
        return context

@method_decorator(login_required, name='dispatch')
class PermisosListView(ListView):
    model = permisos
    template_name = 'core/permisos.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = self.model.objects.all()
        
        if self.request.method == "GET":
            if "search" in self.request.GET:
                name = self.request.GET['search']
                if (name != ''):
                    if len(name.split()) > 1:
                        for x in name.split():
                            object_list = object_list.filter(Q(trabajador__nombre__icontains = x) | Q(trabajador__apellido__icontains = x))
                    else:
                        object_list = object_list.filter(Q(trabajador__nombre__icontains = name) | Q(trabajador__apellido__icontains = name) | Q(trabajador__cedula__icontains = name) | Q(trabajador__cargo__nombre__icontains = name) | Q(trabajador__departamento__nombre__icontains = name) | Q(trabajador__codigo__icontains = name))
            if "permisos" in self.request.GET:
                permiso = self.request.GET['permisos']
                if permiso != "0":
                    object_list = object_list.filter(motivo=permiso)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permisos'] = permisos.tipo_permiso
        return context

@method_decorator(login_required, name='dispatch')
class PermisoDetailView(DetailView):
    model = permisos
    template_name = 'core/permiso_view.html'

@method_decorator(login_required, name='dispatch')
class PermisoUpdate(UpdateView):
    form_class = PermisosForm
    model = permisos
    template_name = 'core/permiso_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        per = permisos.tipo_permiso
        tra = Trabajador.objects.all()
        context["tipo_permiso"] = per
        context["trabajadores"] = tra
        return context
    
    def get_success_url(self):
        return reverse_lazy("core:permiso_view", kwargs={'pk': self.kwargs['pk']})

@method_decorator(login_required, name='dispatch')
class ExtraCreateView(CreateView):
    form_class = ExtrasForm 
    template_name = 'core/extras_add.html'
    success_url = reverse_lazy("core:extras_add")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tra = Trabajador.objects.all()
        context["trabajadores"] = tra
        return context

@method_decorator(login_required, name='dispatch')
class ExtraListView(ListView):
    model = extras
    template_name = 'core/extras.html'
    paginate_by = 10

    def get_queryset(self):
        object_list = self.model.objects.all()
        
        if self.request.method == "GET":
            if "search" in self.request.GET:
                name = self.request.GET['search']
                if (name != ''):
                    if len(name.split()) > 1:
                        for x in name.split():
                            object_list = object_list.filter(Q(trabajador__nombre__icontains = x) | Q(trabajador__apellido__icontains = x))
                    else:
                        object_list = object_list.filter(Q(trabajador__nombre__icontains = name) | Q(trabajador__apellido__icontains = name) | Q(trabajador__cedula__icontains = name))
        return object_list

@method_decorator(login_required, name='dispatch')
class extrasUpdate(UpdateView):
    form_class = ExtrasForm
    model = extras
    template_name = 'core/extras_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tra = Trabajador.objects.all()
        context["trabajadores"] = tra
        return context
    
    def get_success_url(self):
        return reverse_lazy("core:extras")

@method_decorator(login_required, name='dispatch')
class HoyListView(ListView):
    hoy = datetime.now()
    hoy_fecha = hoy.strftime("%Y-%m-%d")
    queryset = marca.objects.filter(fecha = hoy_fecha)
    template_name = 'core/hoy.html'

@login_required
def diarioView(request):
    dep = departamento.objects.all()
    trabajadores = Trabajador.objects.all()
    list_t = {}
    list_tt = []
    if request.POST:
        desde, hasta = request.POST['reservation'].split('-')
        desde = desde.strip(' ')
        hasta = hasta.strip(' ')
        desde = datetime.strptime(desde, '%d/%m/%Y')
        hasta = datetime.strptime(hasta, '%d/%m/%Y')
        print(desde.strftime('%Y-%m-%d 00:00:01'))
        print(hasta.strftime('%Y-%m-%d 23:59:59'))
        p = permisos.objects.filter(Q(desde__range = (desde.strftime('%Y-%m-%d 00:00:01'),hasta.strftime('%Y-%m-%d 23:59:59'))) | Q(hasta__range = (desde.strftime('%Y-%m-%d 00:00:01'),hasta.strftime('%Y-%m-%d 23:59:59'))))
        result = marca.objects.filter(fecha__gte = desde.strftime('%Y-%m-%d 00:00:0'),fecha__lte = hasta.strftime('%Y-%m-%d 23:59:59'))
        if request.POST['departamento'] != "0":
            result = result.filter(trabajador__departamento = request.POST['departamento'])
    else:
        hoy = datetime.now()
        desde = hoy.strftime("%Y-%m-%d 00:00:00")
        hasta = hoy.strftime("%Y-%m-%d 23:59:59")
        result = marca.objects.filter(fecha__gte = desde,fecha__lte = hasta)
        p = permisos.objects.filter(hasta__lte = hasta )
    
    
    for trabajador in trabajadores:
        if result.filter(trabajador = trabajador.user).exists():
            results = result.filter(trabajador = trabajador.user)
            tiene_g = False
            if guardia.objects.filter(trabajador=trabajador.user).exists():
                g = guardia.objects.filter(trabajador=trabajador.user)
                tiene_g = True
            total = results.count()
            if total > 1:
                if total % 2 != 0:
                    total -= 1
                i = 0
                tiempo = 0
                gt = 0
                while(i < total):
                    if tiene_g:
                        if g.count() > 0:
                            for j in g:
                                if j.entrada.date() == results[i+1].fecha.date():
                                    gt += (results[i].fecha - results[i+1].fecha).total_seconds()
                    tiempo += (results[i].fecha - results[i+1].fecha).total_seconds()
                    i += 2
                tiempo -= gt
                list_t['tiempo'] = tiempo
                list_t['trabajador'] = trabajador
                list_t['horas'] = int(tiempo // 3600)
                list_t['segundos'] = int(tiempo % 3600)
                list_t['minutos'] = int(list_t['segundos'] // 60)
                list_t['segundos'] = int(list_t['segundos'] % 60)
                list_t['gt'] = gt
                list_t['horasg'] = int(gt // 3600)
                list_t['segundosg'] = int(gt % 3600)
                list_t['minutosg'] = int(list_t['segundosg'] // 60)
                list_t['segundosg'] = int(list_t['segundosg'] % 60)
                list_tt.append(list_t.copy())
    return render(request,'core/diario.html',{'object_list':result,'departamento':dep,'trabajadores':list_tt, 'permisos':p})

@login_required        
def fechaView(request):
    trabajadores = Trabajador.objects.all()
    dep = departamento.objects.all()
    list_t = {}
    list_tt = []
    for trabajador in trabajadores:
        if marca.objects.filter(trabajador = trabajador.user).exists():
            results = marca.objects.filter(trabajador = trabajador.user)
            if request.POST:
                desde, hasta = request.POST['reservation'].split('-')
                desde = desde.strip(' ')
                hasta = hasta.strip(' ')
                desde = datetime.strptime(desde, '%d/%m/%Y')
                hasta = datetime.strptime(hasta, '%d/%m/%Y')
                results = results.filter(fecha__gte = desde.strftime('%Y-%m-%d 00:00:00'),fecha__lte = hasta.strftime('%Y-%m-%d 23:59:59'))
            total = results.count()
            if total > 1:
                if total % 2 != 0:
                    total -= 1
                i = 0
                tiempo = 0
                extra = 0
                while(i < total):
                    tiempo += (results[i].fecha - results[i+1].fecha).total_seconds()
                    i += 2
                list_t['trabajador'] = trabajador
                list_t['horas'] = int(tiempo // 3600)
                list_t['segundos'] = int(tiempo % 3600)
                list_t['minutos'] = int(list_t['segundos'] // 60)
                list_t['segundos'] = int(list_t['segundos'] % 60)
                list_tt.append(list_t.copy())

    return render(request,'core/fecha.html',{'trabajadores':list_tt,'departamento':dep})

class ReportePDFView(PDFTemplateView):
    template_name = 'core/reporte_pdf.html'

    base_url = 'file://' + settings.STATIC_ROOT
    # download_filename = 'presupuesto.pdf'
    def get_context_data(self, **kwargs):
        dep = departamento.objects.all()
        trabajadores = Trabajador.objects.all()
        list_t = {}
        list_tt = []
        fecha = 0
        depa = "Todos"
        if "fecha" in self.request.GET:
            fecha = self.request.GET['fecha']
            desde, hasta = self.request.GET['fecha'].split('-')
            desde = desde.strip(' ')
            hasta = hasta.strip(' ')
            desde = datetime.strptime(desde, '%d/%m/%Y')
            hasta = datetime.strptime(hasta, '%d/%m/%Y')
            p = permisos.objects.filter(desde__gte = desde.strftime('%Y-%m-%d 00:00:00'), hasta__lte = hasta.strftime('%Y-%m-%d 23:59:59') )
            result = marca.objects.filter(fecha__gte = desde.strftime('%Y-%m-%d 00:00:00'),fecha__lte = hasta.strftime('%Y-%m-%d 23:59:59'))
            if self.request.GET['departamento'] != "0":
                depa = departamento.objects.get(pk = self.request.GET['departamento']).nombre
                result = result.filter(trabajador__get_profile__departamento = self.request.GET['departamento'])
        else:
            hoy = datetime.now()
            desde = hoy.strftime("%Y-%m-%d 00:00:00")
            hasta = hoy.strftime("%Y-%m-%d 23:59:59")
            result = marca.objects.filter(fecha__gte = desde,fecha__lte = hasta)
            p = permisos.objects.filter(desde__gte = desde, hasta__lte = hasta )
        
        
        for trabajador in trabajadores:
            if result.filter(trabajador = trabajador.user).exists():
                results = result.filter(trabajador = trabajador.user)
                tiene_g = False
                if guardia.objects.filter(trabajador=trabajador.user).exists():
                    g = guardia.objects.filter(trabajador=trabajador.user)
                    tiene_g = True
                total = results.count()
                if total > 1:
                    if total % 2 != 0:
                        total -= 1
                    i = 0
                    tiempo = 0
                    gt = 0
                    while(i < total):
                        if tiene_g:
                            if g.count() > 0:
                                for j in g:
                                    if j.entrada.date() == results[i+1].fecha.date():
                                        gt += (results[i].fecha - results[i+1].fecha).total_seconds()
                        tiempo += (results[i].fecha - results[i+1].fecha).total_seconds()
                        i += 2
                    tiempo -= gt
                    list_t['tiempo'] = tiempo
                    list_t['trabajador'] = trabajador
                    list_t['horas'] = int(tiempo // 3600)
                    list_t['segundos'] = int(tiempo % 3600)
                    list_t['minutos'] = int(list_t['segundos'] // 60)
                    list_t['segundos'] = int(list_t['segundos'] % 60)
                    list_t['gt'] = gt
                    list_t['horasg'] = int(gt // 3600)
                    list_t['segundosg'] = int(gt % 3600)
                    list_t['minutosg'] = int(list_t['segundosg'] // 60)
                    list_t['segundosg'] = int(list_t['segundosg'] % 60)
                    list_tt.append(list_t.copy())
        return super(ReportePDFView, self).get_context_data(
            departamento = depa,
            fecha = fecha,
            permisos=p,
            object_list=result,
            trabajadores=list_tt,
            pagesize='letter',
            title='Presupuesto',
            **kwargs
        )

@login_required
def exportarhora(request):
    # Obtenemos la fecha para agregarla al nombre del archivo
    dep = departamento.objects.all()
    trabajadores = Trabajador.objects.all()
    list_t = {}
    list_tt = []
    if request.POST:
        desde, hasta = request.POST['reservation'].split('-')
        desde = desde.strip(' ')
        hasta = hasta.strip(' ')
        desde = datetime.strptime(desde, '%d/%m/%Y')
        hasta = datetime.strptime(hasta, '%d/%m/%Y')
        p = permisos.objects.filter(desde__gte = desde.strftime('%Y-%m-%d 00:00:00'), hasta__lte = hasta.strftime('%Y-%m-%d 23:59:59') )
        result = marca.objects.filter(fecha__gte = desde.strftime('%Y-%m-%d 00:00:00'),fecha__lte = hasta.strftime('%Y-%m-%d 23:59:59'))
        if request.POST['departamento'] != "0":
            result = result.filter(trabajador__departamento = request.POST['departamento'])
    else:
        hoy = datetime.now()
        desde = hoy.strftime("%Y-%m-%d 00:00:00")
        hasta = hoy.strftime("%Y-%m-%d 23:59:59")
        result = marca.objects.filter(fecha__gte = desde,fecha__lte = hasta)
        p = permisos.objects.filter(desde__gte = desde, hasta__lte = hasta )
    
    
    for trabajador in trabajadores:
        if result.filter(trabajador = trabajador.user).exists():
            results = result.filter(trabajador = trabajador.user)
            tiene_g = False
            if guardia.objects.filter(trabajador=trabajador.user).exists():
                g = guardia.objects.filter(trabajador=trabajador.user)
                tiene_g = True
            total = results.count()
            if total > 1:
                if total % 2 != 0:
                    total -= 1
                i = 0
                tiempo = 0
                gt = 0
                while(i < total):
                    if tiene_g:
                        if g.count() > 0:
                            for j in g:
                                if j.entrada.date() == results[i+1].fecha.date():
                                    gt += (results[i].fecha - results[i+1].fecha).total_seconds()
                    tiempo += (results[i].fecha - results[i+1].fecha).total_seconds()
                    i += 2
                tiempo -= gt
                list_t['tiempo'] = tiempo
                list_t['trabajador'] = trabajador
                list_t['horas'] = int(tiempo // 3600)
                list_t['segundos'] = int(tiempo % 3600)
                list_t['minutos'] = int(list_t['segundos'] // 60)
                list_t['segundos'] = int(list_t['segundos'] % 60)
                list_t['gt'] = gt
                list_t['horasg'] = int(gt // 3600)
                list_t['segundosg'] = int(gt % 3600)
                list_t['minutosg'] = int(list_t['segundosg'] // 60)
                list_t['segundosg'] = int(list_t['segundosg'] % 60)
                list_tt.append(list_t.copy())
    export = []
    # Se agregan los encabezados de las columnas
    export.append([
        'C.I.',
        'Nombre y Apellido',
        'Cargo',
        'Departamento',
        'Tipo',
        'Fecha',
        'Hora',
    ])
    for hora in result:
        export.append([
            hora.trabajador.cedula,
            "{} {}".format(hora.trabajador.first_name,hora.trabajador.last_name),
            hora.trabajador.cargo.nombre,
            hora.trabajador.departamento.nombre,
            hora.get_tipo_display(),
            "{:%d/%m/%Y}".format(hora.fecha),
            "{:%I:%M:%S %P}".format(hora.fecha),
        ])
    export.append([])
    
    export.append([
        'C.I.',
        'Nombre y Apellido',
        'Cargo',
        'Departamento',
        'Horas TR',
        'Horas TG',
    ])

    for hora in list_tt:
        export.append([
            hora['trabajador'].cedula,
            "{} {}".format(hora['trabajador'].user.first_name,hora['trabajador'].user.last_name),
            hora['trabajador'].cargo,
            hora['trabajador'].departamento.nombre,
            "{:02d}:{:02d}:{:02d}".format(hora['horas'],hora['minutos'],hora['segundos']),
            "{:02d}:{:02d}:{:02d}".format(hora['horasg'],hora['minutosg'],hora['segundosg']),
        ])
    export.append([])
        # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
        # acceder a campos con relaciones y no solo al id
    
    
    export.append([
        'C.I.',
        'Nombre y Apellido',
        'Cargo',
        'Departamento',
        'Motivo',
        'Observación',
        'Fecha',
    ])

    for permiso in p:
        export.append([
            permiso.trabajador.cedula,
            "{} {}".format(permiso.trabajador.first_name,permiso.trabajador.last_name),
            permiso.trabajador.cargo.nombre,
            permiso.trabajador.departamento.nombre,
            permiso.get_motivo_display(),
            permiso.observacion,
            "{:%d/%m/%Y} - {:%d/%m/%Y}".format(permiso.desde, permiso.hasta),
        ])
    export.append([])

    today    = datetime.now()
    strToday = today.strftime("%Y%m%d")

    # se transforma el array a una hoja de calculo en memoria
    sheet = excel.pe.Sheet(export)

    
    # se devuelve como "Response" el archivo para que se pueda "guardar"
    # en el navegador, es decir como hacer un "Download"
    return excel.make_response(sheet, "xlsx", file_name="reporte_excel")

def visitantesAdd(request):
    form = VisitarntesForm()
    dep = departamento.objects.all()
    if request.method == 'POST':
        form = VisitarntesForm(request.POST)
        if form.is_valid():
            if request.POST['tipo'] == "Entrada":
                tipo = "E"
            else:
                tipo = "S"
            m = form.save()
            m.tipo = tipo
            m.save()
            return render(request,'core/visitante_add.html',{'form':form,'marca':tipo, 'hora':m.fecha})
    return render(request,'core/visitante_add.html',{'form':form,'departamento':dep})

@method_decorator(login_required, name='dispatch')
class VisitasListView(ListView):
    model = visitantes
    template_name = 'core/visitas.html'
    success_url = reverse_lazy("core:visitas")

    def get_queryset(self):
        if self.request.GET:
            desde, hasta = self.request.GET['reservation'].split('-')
            desde = desde.strip(' ')
            hasta = hasta.strip(' ')
            desde = datetime.strptime(desde, '%d/%m/%Y')
            hasta = datetime.strptime(hasta, '%d/%m/%Y')
            object_list = self.model.objects.filter(fecha__gte = desde.strftime('%Y-%m-%d 00:00:00'),fecha__lte = hasta.strftime('%Y-%m-%d 23:59:59'))
            if self.request.GET['departamento'] != "0":
                object_list = object_list.filter(departamento = self.request.GET['departamento'])
            
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dep = departamento.objects.all()
        context["departamento"] = dep
        return context

