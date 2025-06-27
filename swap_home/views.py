from django.shortcuts import render,redirect
from .models import *
from .forms import *
from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login


# -- VISTA INICIAL --
def index(request):
    return render(request, "index.html")

# -- LOGIN --
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                # Redirigimos según el tipo de usuario
                #if user.is_superuser or user.is_staff:
                if user.is_superuser:
                    return redirect('/admin/')  # lo mandamos al panel
                elif user.groups.filter(name='TTHH').exists():
                    return redirect('tthh')
                elif user.groups.filter(name='Informatica').exists():
                    return redirect('informatica')
                elif user.groups.filter(name='Porteria').exists():
                    return redirect('porteria')
                elif user.groups.filter(name='Tecnico').exists():
                    return redirect('tecnico')
                elif user.groups.filter(name='ServicioTecnico').exists():
                    return redirect('serviciotecnico')
                else:
                    messages.error(request, 'Tu cuenta no tiene un grupo asignado.')
                    return redirect('login')  # o una vista de error personalizada
            else:
                messages.error(request, 'Tu cuenta está desactivada.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'auth_/login.html')

from django.contrib.auth import logout
# -- LOGOUT --
def logout_view(request):
    logout(request)
    return redirect('login')



