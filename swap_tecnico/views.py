
from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.utils import timezone

from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *
from .forms import *
# Create your views here.

# --- Proteger de otros Usuarios Logeados ---
def is_swap_tecnico(user):
    if not user.groups.filter(name='Tecnico').exists():
        return False

    now = timezone.localtime()

    # Bloquear desde el día 11 hasta el 14 inclusive
    if 10 <= now.day <= 14:
        return False

    return True

def acces_denied(request):
    return render(request, 'acces_denied.html')

# Vista Principal
@login_required
@user_passes_test(is_swap_tecnico, login_url='acces_denied')
def tecnico(request):
    tarea = Tareas.objects.filter(tarea_dpto__dpto_nombre="General")
    tarea_dia = Tareadia.objects.filter(td_dia="General")
    
    return render(request, 'tecnico.html',{
        'tarea': tarea,
        'dia': tarea_dia,
    })
    
# Cargacion de la trabajacion
@login_required
@user_passes_test(is_swap_tecnico, login_url='acces_denied')
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
class VerCTListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "verct.html"
    context_object_name = "trabajos"
    paginate_by = 25  # ajusta a gusto

    def test_func(self):
        return is_swap_tecnico(self.request.user)

    def handle_no_permission(self):
        return redirect("acces_denied")

    def _nombre_tecnico(self):
        user = self.request.user
        nombre_tecnico = f"{(user.first_name or '').strip()} {(user.last_name or '').strip()}".strip()
        primer_nombre = (user.first_name or "").split(" ")[0].strip()
        primer_apellido = (user.last_name or "").split(" ")[0].strip()
        nombre_simple = f"{primer_nombre} {primer_apellido}".strip()
        return nombre_tecnico, nombre_simple

    def get_queryset(self):
        nombre_tecnico, nombre_simple = self._nombre_tecnico()

        # Base queryset: primero intenta match exacto (más rápido)
        qs = Tecnicos.objects.all()
        if nombre_tecnico:
            qs_exact = qs.filter(tec_nombre=nombre_tecnico)
            qs = qs_exact if qs_exact.exists() else qs.filter(tec_nombre__icontains=nombre_simple)
        else:
            # si el user no tiene nombre/apellido, no devolvemos nada
            return Tecnicos.objects.none()

        # filtros de fecha
        fecha = (self.request.GET.get("fecha") or "").strip()
        fecha_desde = (self.request.GET.get("fecha_desde") or "").strip()
        fecha_hasta = (self.request.GET.get("fecha_hasta") or "").strip()

        # prioridad: fecha exacta > rango
        if fecha:
            qs = qs.filter(tec_fecha=fecha)
        else:
            if fecha_desde:
                qs = qs.filter(tec_fecha__gte=fecha_desde)
            if fecha_hasta:
                qs = qs.filter(tec_fecha__lte=fecha_hasta)

        # orden estable
        return qs.order_by("-tec_fecha", "-tec_id")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        nombre_tecnico, nombre_simple = self._nombre_tecnico()

        ctx["nombre_tecnico"] = nombre_tecnico
        ctx["nombre_simple"] = nombre_simple

        # valores actuales (para mantener inputs)
        ctx["fecha_actual"] = (self.request.GET.get("fecha") or "").strip()
        ctx["fecha_desde"] = (self.request.GET.get("fecha_desde") or "").strip()
        ctx["fecha_hasta"] = (self.request.GET.get("fecha_hasta") or "").strip()

        # para construir links de paginación conservando filtros
        q = self.request.GET.copy()
        q.pop("page", None)
        ctx["querystring_sin_page"] = q.urlencode()

        return ctx

    
    
    
    
    