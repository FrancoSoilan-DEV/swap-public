from django.shortcuts import render,redirect
from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *
from .forms import *
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

# --- Proteger de otros Usuarios Logeados ---
def is_swap_tecnico(user):
    return user.groups.filter(name='Tecnico').exists()


# Vista Principal
@login_required
@user_passes_test(is_swap_tecnico)
def tecnico(request):
    tarea = Tareas.objects.filter(tarea_dpto__dpto_nombre="General")
    tarea_dia = Tareadia.objects.filter(td_dia="General")
    
    return render(request, 'tecnico.html',{
        'tarea': tarea,
        'dia': tarea_dia,
    })
    
# Cargacion de la trabajacion
@login_required
@user_passes_test(is_swap_tecnico)
def cargar_trabajo(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            trabajo = form.save(commit=False)
            
            
            # Guardar fecha y hora exactas actuales
            trabajo.tec_fexacta = datetime.now().date()
            trabajo.tec_hexacta = datetime.now().time()

            # Valor por defecto: Estadoentrada = "Pendiente⚠️"
            estado_defecto = Estadoentrada.objects.get(ee_estado="Pendiente⚠️")
            trabajo.tec_ee = estado_defecto

            # Valor por defecto: monto = 0
            monto_defecto = Tecnicosmonto.objects.get(tm_monto=0)
            trabajo.tec_tm = monto_defecto

            # Nombre segun loggeo
            # Asignar nombre del técnico (nombre + apellido del usuario logueado)
            trabajo.tec_nombre = f"{request.user.first_name} {request.user.last_name}"
            
            trabajo.save()
            return redirect('ct')  # Redirige a la misma u otra vista

    else:
        form = TecnicoForm()

    return render(request, "cargar_trabajo.html", {"form": form})

# Se ve los trabajos realizados
@login_required
@user_passes_test(is_swap_tecnico)
def verct(request):
    user = request.user
    nombre_tecnico = f"{user.first_name} {user.last_name}"
    primer_nombre = user.first_name.split(" ")[0]
    primer_apellido = user.last_name.split(" ")[0]
    nombre_simple = f"{primer_nombre} {primer_apellido}"
    # Parámetros de fecha
    fecha = request.GET.get("fecha")
    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")

    # Base queryset filtrado por el técnico actual
    trabajos = Tecnicos.objects.filter(tec_nombre=nombre_tecnico)

    # Aplicar filtros de fecha
    if fecha:
        trabajos = trabajos.filter(tec_fecha=fecha)

    if fecha_desde:
        trabajos = trabajos.filter(tec_fecha__gte=fecha_desde)

    if fecha_hasta:
        trabajos = trabajos.filter(tec_fecha__lte=fecha_hasta)

    return render(request, "verct.html", {
        "trabajos": trabajos,
        "nombre_tecnico": nombre_tecnico,
        "fecha_actual": fecha or "",
        "fecha_desde": fecha_desde or "",
        "fecha_hasta": fecha_hasta or "",
        "nombre_simple":nombre_simple,
    })
    
    