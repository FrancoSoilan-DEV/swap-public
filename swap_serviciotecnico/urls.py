from django.urls import path
from swap_serviciotecnico import views

urlpatterns = [
    path("", views.serviciotecnico, name="serviciotecnico"),
    path("Ver/", views.veregistro, name="veregistro"),
    path("Ver/NuevoMonto/", views.addmonto, name="addmonto"),
    path('editar_trabajo/<int:tec_id>/', views.editar_trabajo, name='editar_trabajo'),
    path("Historial/", views.historial, name="historial"),
    path('e-e/', views.e_e, name='e_e'),
    path('editar-trabajos/bulk/', views.editar_trabajos_bulk, name='editar_trabajos_bulk'),

]