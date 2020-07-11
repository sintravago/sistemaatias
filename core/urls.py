from django.urls import include, path
from . import views


core_patterns = ([
    path('', views.marcar, name ='index'),
    path('trabajadores/', views.TrabajadoresListView.as_view(), name ='trabajadores'),
    path('reporte/diario/', views.diarioView, name ='diario'),
    path('reporte/fecha', views.fechaView, name ='fecha'),
], 'core')

urlpatterns = [
    path('', include(core_patterns)),
]