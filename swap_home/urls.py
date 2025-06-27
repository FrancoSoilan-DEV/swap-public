from django.urls import path
from swap_home import views


urlpatterns = [
    #path("",views.index,name="index"),
    #auth
    path("", views.login_view, name="login"),
    #redirigir a un template lindo en caso de intentar ingresar a otro lugar donde no corresponde
    #path('acceso-denegado/', views.acceso_denegado, name='acceso_denegado'),
    path('logout/', views.logout_view, name='logout'),
]
