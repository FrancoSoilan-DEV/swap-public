from django.urls import path
from swap_tthh import views
from django.contrib import admin




urlpatterns = [
    
    #vista principal
    path('', views.tthh, name='tthh'),
    path("actualizar_estado/<int:tarea_id>/", views.actualizar_estado, name="actualizar_estatus"),
    path("porteria/funcionarios",views.registro_entrada, name="registro_entrada"),
    path('exportar_funcionarios/', views.exportar_excel_funcionario, name='exportar_excel_funcionarios'),  # Nueva ruta
    path("porteria/proveedores/",  views.proveedores, name="proveedores"),
    path("exportar_proveedores/", views.exportar_excel_proveedores, name="exportar_proveedores"),
    path("porteria/cobradores/", views.cobradores, name="cobradores"),
    path("exportar_cobradores/", views.exportar_excel_cobradores, name="exportar_excel_cobradores"),
    path("ex_excel/", views.ex_excel, name="ex_excel"),
    path("TrabajosServicioTecnico/", views.vistast, name="vistast"),
    path("porteria/visitas/", views.visitas, name="visitas"),
    path('porteria/visitas/exportar/', views.exportar_visitas_excel, name='exportar_visitas_excel'),
    path("funcionarios/", views.funcionarios, name="tthhfunc"),
    path("excel-nomina/", views.exportar_nomina, name="exp-nom"),
    path('admin/', admin.site.urls),
    path("funcionarios/telefonos", views.telefonos, name="telefonos"),
    path('exportar-pdf/', views.exportar_pdf, name='exp-tel'),
    path("funcionarios/ExFuncionarios", views.ex_funcionarios, name="ex_funcionarios"),
]