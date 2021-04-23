from django.urls import include, path
from . import views


pagos_patterns = ([
    path('factura/add', views.FacturaCreateView.as_view(), name ='factura_add'),
    path('facturas/', views.FacturaListView.as_view(), name ='facturas'),
    path('facturas/view/<int:pk>', views.FacturaDetailView.as_view(), name ='factura_view'),
    path('facturas/edit/<int:pk>', views.FacturaUpdate.as_view(), name ='factura_edit'),
    path('facturas/edite/<int:pk>', views.FacturaUpdatestatus.as_view(), name ='factura_edite'),
    path('reporte/', views.ReporteView.as_view(), name ='reporte'),
], 'pagos')

urlpatterns = [
    path('', include(pagos_patterns)),
]