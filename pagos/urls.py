from django.urls import include, path
from . import views


pagos_patterns = ([
    path('factura/add', views.FacturaCreateView.as_view(), name ='factura_add'),
    path('facturas/', views.FacturaListView.as_view(), name ='facturas'),
    path('facturas/update/<int:pk>', views.facturaStatusUpdate, name ='facturas_update'),
    path('facturas/update2/<int:pk>', views.facturaStatusUpdate2, name ='facturas_update2'),
    path('facturas/view/<int:pk>', views.FacturaDetailView.as_view(), name ='factura_view'),
    path('facturas/edit/<int:pk>', views.FacturaUpdate.as_view(), name ='factura_edit'),
    path('reporte/', views.ReporteView.as_view(), name ='reporte'),
], 'pagos')

urlpatterns = [
    path('', include(pagos_patterns)),
]