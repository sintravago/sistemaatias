from django.shortcuts import render
from .forms import MarcarForm
from registration.models import Profile, horario
from .models import marca
from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.db.models import Avg, Count, Min, Sum
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Create your views here.

def marcar(request):
    form = MarcarForm()
    if request.method == 'POST':
        form = MarcarForm(request.POST)
        if form.is_valid():
            if (Profile.objects.filter(cedula=form.cleaned_data['barcode']).exists()):
                trabajador = Profile.objects.get(cedula=form.cleaned_data['barcode'])
                if 'entrada' in request.POST:
                    e = "E"
                else:
                    e = "S"
                if marca.objects.filter(trabajador=trabajador.user).exists():
                    ultima = marca.objects.filter(trabajador=trabajador.user).first()
                    if ultima.tipo == e:
                        return render(request,'core/marcar.html',{'form':form, 'marca':'ya', 'e': e})
                m = marca(trabajador=trabajador.user, tipo=e)
                m.save()
                return render(request,'core/marcar.html',{'form':form, 'trabajador':trabajador, 'marca':e, 'hora':m.fecha})
            else:
                return render(request,'core/marcar.html',{'form':form, 'marca':'no'})
    return render(request,'core/marcar.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class TrabajadoresListView(ListView):
    model = Profile
    template_name = 'core/trabajadores.html'

@method_decorator(login_required, name='dispatch')
class HoyListView(ListView):
    hoy = datetime.now()
    hoy_fecha = hoy.strftime("%Y-%m-%d")
    queryset = marca.objects.filter(fecha = hoy_fecha)
    template_name = 'core/hoy.html'

@login_required
def diarioView(request):
    if request.POST:
        fecha = request.POST['date']
        fecha_f = datetime.strptime(fecha, '%d/%m/%Y')
        result = marca.objects.filter(fecha = fecha_f.strftime('%Y-%m-%d'))
    else:
        hoy = datetime.now()
        hoy_fecha = hoy.strftime("%Y-%m-%d")
        result = marca.objects.filter(fecha = hoy_fecha)
    return render(request,'core/diario.html',{'object_list':result})

@login_required        
def fechaView(request):
    if request.POST:
        # result = horas.objects.filter(fecha=request.POST['reservation']).order_by('trabajador')
        inicio, fin = request.POST['reservation'].split('-')
        inicio = inicio.strip(' ')
        fin = fin.strip(' ')
        inicio_f = datetime.strptime(inicio, '%d/%m/%Y')
        fin_f = datetime.strptime(fin, '%d/%m/%Y')
        result = marca.objects.filter(fecha__gte=inicio_f.strftime('%Y-%m-%d'),fecha__lte=fin_f.strftime('%Y-%m-%d')).order_by('trabajador')
    else:
        result = marca.objects.all().order_by('trabajador')
    trabajadores = []
    trabajador = {}
    for hora in result:
        if len(trabajadores) == 0 or trabajadores[-1]['trabajador'] != hora.trabajador:
            trabajador['trabajador'] = hora.trabajador
            if hora.salida:
                trabajador['total'] = (hora.salida.hour * 3600 + hora.salida.minute * 60 + hora.salida.second) - (hora.entrada.hour * 3600 + hora.entrada.minute * 60 + hora.entrada.second)
            else:
                trabajador['total'] = 0
            trabajador['minutos'] = int(trabajador['total'] / 60)
            trabajador['segundos'] = int(trabajador['total'] % 60)
            trabajador['horas'] = int(trabajador['minutos'] / 60)
            trabajador['minutos'] = int(trabajador['minutos'] % 60)
            trabajadores.append(trabajador.copy())
        else:
            if hora.salida:
                trabajadores[-1]['total'] += (hora.salida.hour * 3600 + hora.salida.minute * 60 + hora.salida.second) - (hora.entrada.hour * 3600 + hora.entrada.minute * 60 + hora.entrada.second)
                trabajadores[-1]['minutos'] = int(trabajadores[-1]['total'] / 60)
                trabajadores[-1]['segundos'] = int(trabajadores[-1]['total'] % 60)
                trabajadores[-1]['horas'] = int(trabajadores[-1]['minutos'] / 60)
                trabajadores[-1]['minutos'] = int(trabajadores[-1]['minutos'] % 60)
    return render(request,'core/fecha.html',{'trabajadores':trabajadores})

            
        
        
        