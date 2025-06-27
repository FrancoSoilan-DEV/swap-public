from django.urls import path
from swap_tecnico import views

urlpatterns = [
    path("", views.tecnico, name="tecnico"),
    path("cargar/", views.cargar_trabajo, name="ct"),
    path("ver", views.verct, name="verct"),
]