
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("swap_home.urls")),
    path("informatica/", include("swap_informatica.urls")),
    path("tthh/", include("swap_tthh.urls")),
    path("porteria/", include("swap_porteria.urls")),
    path("tecnico/", include("swap_tecnico.urls")),
    path("ServicioTecnico/", include("swap_serviciotecnico.urls")),
]

