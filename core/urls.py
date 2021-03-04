from django.urls import include, path
from . import views


core_patterns = ([
    path('', views.marcar, name ='index'),
    path('trabajadores/search', views.TrabajadoresListView.as_view(), name ='trabajadores'),
    path('trabajadores/add', views.TrabajadorCreateView.as_view(), name ='trabajador_add'),
    path('trabajadores/edit/<int:pk>', views.TrabajadorUpdate.as_view(), name ='trabajador_edit'),
    path('permisos/add', views.PermisosCreateView.as_view(), name ='permiso_add'),
    path('permisos/view/<int:pk>', views.PermisoDetailView.as_view(), name ='permiso_view'),
    path('permisos/edit/<int:pk>', views.PermisoUpdate.as_view(), name ='permiso_edit'),
    path('permisos/search', views.PermisosListView.as_view(), name ='permisos'),
    path('trabajadores/view/<int:pk>', views.TrabajadorDetailView.as_view(), name ='trabajador_view'),
    path('reportepdf/', views.ReportePDFView.as_view(), name ='pdf'),
    path('reportexcel/', views.exportarhora, name ='excel'),
    path('reporte/diario/', views.diarioView, name ='diario'),
    path('reporte/fecha', views.fechaView, name ='fecha'),
    path('visitante/add', views.visitantesAdd, name ='visitante_add'),
    path('extras/add', views.ExtraCreateView.as_view(), name ='extras_add'),
    path('extras/search', views.ExtraListView.as_view(), name ='extras'),
    path('extras/edit/<int:pk>', views.extrasUpdate.as_view(), name ='extras_edit'),
    path('visitantes', views.VisitasListView.as_view(), name ='visitas'),

], 'core')

urlpatterns = [
    path('', include(core_patterns)),
]