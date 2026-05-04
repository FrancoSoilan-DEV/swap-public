from django.urls import path
from swap_informatica import views
from swap_informatica.views import InformaticaDashboardView

urlpatterns = [
    
    #vista principal
    path('', InformaticaDashboardView.as_view(), name='informatica'),

    #==============================================================================#
    
    #redirigir a BACKUPS
    path('backups/', views.backups, name="backups"),
    
    
    path('backups/semanales/', views.backups_semanales, name='backups-semanales'),

    path('backups/asignacion/', views.bk_asignacion, name='bk-asignacion'),
    
    #AÑADIR FUNCIONARIO CON EQUIPO
    path("backups/configuracion", views.bk_configuracion, name="config-equipos"),
    
    #GUARDAR LOS BACKUPS HECHOS
    path("bkhecho/", views.agregar_backups_hechos, name="bkdone"),
    #REDIRIGIR A OTRA PAGINA DE BKHECHOS
    path("backups/hechos/", views.backups_hechos, name="bk-hechos"),
    
    # Exportar Excel
    path("backups/exportar-excel/", views.exportar_excel_backups, name="exportar-excel-backups"),
    #==============================================================================#
    # Inventario
    path("inventario/", views.inventario, name="inventario"), 
    # añadir deposito
    path("add-deposito/", views.agregar_rak, name="add-rak"),
    # añadir estado
    path("add-status/", views.agregar_status, name="add-status"),
    # añadir item
    path("add-item/", views.agregar_item, name="add-item"),
    # añadir nuevo articulo
    path("addarticle/", views.agregar_articulo, name="add-new-article"),
    # actualizar inventario
    path("guardar_cantidad/", views.guardar_cantidad, name="guardar_cantidad"),
    # inventario de equipos
    path("inventario/equipos/", views.equipos, name="equipos"),
    # pagina de equipos
    # añadir nuevo equipo
    path('inventario/equipos/nuevo/', views.NuevoEquipo, name='nuevo_equipo'),
    
    #==============================================================================#
    # Mantenimiento
    path("mantenimiento/", views.mantenimiento, name="mantenimiento"),
    # cambiar estado
    path('mantenimientos/cambiar_estado/<int:mc_id>/', views.cambiar_estado_mantenimiento, name='cambiar_estado_mantenimiento'),
    # añadir mantenimiento
    path("mantenimiento/add/", views.addmantenimiento, name="addmantenimiento"),
    #==============================================================================#
    
]