from django.urls import path
from swap_tecnico import views
from swap_tecnico.views import VerCTListView

urlpatterns = [
    path("", views.tecnico, name="tecnico"),
    path("cargar/", views.cargar_trabajo, name="ct"),
    path("ver/", VerCTListView.as_view(), name="verct"),
]