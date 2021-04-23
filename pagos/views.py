from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from .forms import FacturaForm
from .models import factura
from django.db.models import F

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


