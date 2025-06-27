from django.urls import path
from swap_informatica import views

from django.contrib.auth.decorators import login_required



from django.contrib.auth import views as auth_views
urlpatterns = [
    
    #vista principal
    path('', views.informatica, name='informatica'),
    #actualizar estado TAREA SEMANAL
    path("actualizar_estado/<int:tarea_id>/", views.actualizar_estado, name="actualizar_estado"),
    
    
    #==============================================================================#
    
    #redirigir a BACKUPS
    path('backups/', views.backups, name="backups"),
    
    #actualizar estado BACKUP
    path("actualizar_estado_bk/<int:bp_id>/", views.actualizar_estado_bk, name="actualizar_estado_bk" ),
    
    #AÑADIR/ELIMINAR BACKUP SEMANAL
    path("add-bk/", views.add_backup, name="add_backup"),
    #path("delete-bk/", views.delete_backup, name="delete_backup"),
    
    #AÑADIR BACKUP A FUNCIONARIO CON EQUIPO
    path("add-backup/", views.add_bk, name="new_bk"),
    path("delete-backup/", views.delete_bk, name="delete_bk"),
    
    #AÑADIR FUNCIONARIO CON EQUIPO
    path("add-fce/", views.add_fce, name="add_fce"),
    path("delete-fce/", views.delete_fce, name="delete_fce"),
    
    #GUARDAR LOS BACKUPS HECHOS
    path("bkhecho/", views.agregar_backups_hechos, name="bkdone"),
    #REDIRIGIR A OTRA PAGINA DE BKHECHOS
    path("backups/hechos/", views.bkhechos, name="bk-hechos"),
    path('eliminar-backups/', views.eliminar_backups, name='eliminar-backups'),
    
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
    


     
    #path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
]