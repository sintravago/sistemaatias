from django.urls import include, path
from . import views


pagos_patterns = ([
    path('factura/add', views.FacturaCreateView.as_view(), name ='factura_add'),
    path('facturas/', views.FacturaListView.as_view(), name ='facturas'),
], 'pagos')

urlpatterns = [
    path('', include(pagos_patterns)),
]