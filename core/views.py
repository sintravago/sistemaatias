from django.shortcuts import render
from .forms import HorarioAddForm
from .models import Trabajador, horas
from datetime import datetime
from django.views.generic.list import ListView
from django.db.models import Avg, Count, Min, Sum
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

def marcar(request):
    form = HorarioAddForm()
    if request.method == 'POST':
        form = HorarioAddForm(request.POST)
        if form.is_valid():
            if (Trabajador.objects.filter(cedula=form.cleaned_data['barcode']).exists()):
                t = Trabajador.objects.get(cedula=form.cleaned_data['barcode'])
                hoy = datetime.now()
                hoy_fecha = hoy.strftime("%Y-%m-%d")
                if (horas.objects.filter(trabajador = t, fecha = hoy_fecha).exists()):
                    registro = horas.objects.get(trabajador = t, fecha = hoy_fecha)
                    hoy_hora = hoy.strftime("%H:%M:%S")
                    registro.salida = hoy_hora
                    registro.save()
                    return render(request,'core/marcar.html',{'form':form, 'trabajador':t, 'marca':'salida', 'hora':hoy})
                else:
                    registro = horas.objects.create(trabajador = t)
                    return render(request,'core/marcar.html',{'form':form, 'trabajador':t, 'marca':'entrada', 'hora':registro.entrada})
            else:
                return render(request,'core/marcar.html',{'form':form, 'marca':'no'})
    return render(request,'core/marcar.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class TrabajadoresListView(ListView):
    model = Trabajador
    template_name = 'core/trabajadores.html'

@method_decorator(login_required, name='dispatch')
class HoyListView(ListView):
    hoy = datetime.now()
    hoy_fecha = hoy.strftime("%Y-%m-%d")
    queryset = horas.objects.filter(fecha = hoy_fecha)
    template_name = 'core/hoy.html'

@login_required
def diarioView(request):
    if request.POST:
        fecha = request.POST['date']
        fecha_f = datetime.strptime(fecha, '%d/%m/%Y')
        result = horas.objects.filter(fecha = fecha_f.strftime('%Y-%m-%d'))
    else:
        hoy = datetime.now()
        hoy_fecha = hoy.strftime("%Y-%m-%d")
        result = horas.objects.filter(fecha = hoy_fecha)
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
        result = horas.objects.filter(fecha__gte=inicio_f.strftime('%Y-%m-%d'),fecha__lte=fin_f.strftime('%Y-%m-%d')).order_by('trabajador')
    else:
        result = horas.objects.all().order_by('trabajador')
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

            
        
        
        