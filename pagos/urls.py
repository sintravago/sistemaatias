from django.urls import include, path
from . import views


pagos_patterns = ([
    path('empresa/add', views.EmpresaCreateView.as_view(), name ='empresa_add'),
    path('empresa/edit/<int:pk>', views.EmpresaUpdate.as_view(), name ='empresa_edit'),
    path('empresas/', views.EmpresaListView.as_view(), name ='empresas'),
    path('factura/add', views.FacturaCreateView.as_view(), name ='factura_add'),
    path('facturas/', views.FacturaListView.as_view(), name ='facturas'),
    path('facturasp/', views.FacturaspListView.as_view(), name ='facturasp'),
    path('facturaspp/', views.FacturasppListView.as_view(), name ='facturaspp'),
    path('facturas/update/<int:pk>', views.facturaStatusUpdate, name ='facturas_update'),
    path('facturas/update2/<int:pk>', views.facturaStatusUpdate2, name ='facturas_update2'),
    path('facturas/update3/<int:pk>', views.facturaStatusUpdate3, name ='facturas_update3'),
    path('facturas/view/<int:pk>', views.FacturaDetailView.as_view(), name ='factura_view'),
    path('facturas/edit/<int:pk>', views.FacturaUpdate.as_view(), name ='factura_edit'),
    path('facturas/pdf/<int:pk>', views.FacturaPDFView.as_view(), name ='factura_pdf'),
    path('facturas/exportar', views.exportarfacturas, name ='exportar'),
    path('iva/edit/<int:pk>', views.IvaUpdate.as_view(), name ='iva_edit'),
    path('reporte/', views.ReporteView.as_view(), name ='reporte'),
    path('get_servicio_ajax/', views.get_servicio_ajax, name ='get_servicio_ajax'),
    path('get_islr_ajax/', views.get_islr_ajax, name ='get_islr_ajax'),
], 'pagos')

urlpatterns = [
    path('', include(pagos_patterns)),
]