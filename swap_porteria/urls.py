from django.urls import path
from swap_porteria import views

urlpatterns = [
    path("", views.porteria, name="porteria"),
    path("entrada/", views.cargar, name="cargar"),
    path("entrada/formularios/",views.formularios, name="formularios"),
    path("salida/", views.salida, name="salida"),
    path('editar_entrada/<int:e_id>/', views.editar_entrada, name='editar_entrada'),
    path("ver/", views.ver, name="ver"),
]