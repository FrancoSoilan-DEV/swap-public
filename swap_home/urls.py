from django.urls import path
from swap_home import views


urlpatterns = [
    path("", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
]
