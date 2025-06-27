from django.shortcuts import render,redirect,get_object_or_404
from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *
from swap_porteria.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

# --- Proteger de otros Usuarios Logeados ---
def is_swap_porteria(user):
    return user.groups.filter(name='Porteria').exists()

# menu principal porteria
@login_required
@user_passes_test(is_swap_porteria)
def porteria(request):
    tarea = Tareas.objects.filter(tarea_dpto__dpto_nombre="General")
    tarea_dia = Tareadia.objects.filter(td_dia="General")
    
    
    
    return render(request, 'porteria.html',{
        'tarea': tarea,
        'dia': tarea_dia,
    })

# cargar entradas y opciones a formularios
@login_required
@user_passes_test(is_swap_porteria)
def cargar(request):
    entrada_funcionario = EntradaFuncionario()
    entrada_cobrador = EntradaCobrador()
    entrada_proveedor = EntradaProveedor()
    entrada_visita = EntradaVisita()

    if request.method == "POST":
        if 'submit_funcionario' in request.POST:
            entrada_funcionario = EntradaFuncionario(request.POST)
            if entrada_funcionario.is_valid():
                entrada = entrada_funcionario.save(commit=False)
                entrada.e_salida = "00:00"
                entrada.e_ee = Estadoentrada.objects.get(ee_estado="Pendiente⚠️")
                entrada.save()
                return redirect('cargar')

        elif 'submit_cobrador' in request.POST:
            entrada_cobrador = EntradaCobrador(request.POST)
            if entrada_cobrador.is_valid():
                entrada = entrada_cobrador.save(commit=False)
                entrada.e_salida = "00:00"
                entrada.e_ee = Estadoentrada.objects.get(ee_estado="Pendiente⚠️")
                entrada.save()
                return redirect('cargar')

        elif 'submit_proveedor' in request.POST:
            entrada_proveedor = EntradaProveedor(request.POST)
            if entrada_proveedor.is_valid():
                entrada = entrada_proveedor.save(commit=False)
                entrada.e_salida = "00:00"
                entrada.e_ee = Estadoentrada.objects.get(ee_estado="Pendiente⚠️")
                entrada.save()
                return redirect('cargar')

        elif 'submit_visita' in request.POST:
            entrada_visita = EntradaVisita(request.POST)
            if entrada_visita.is_valid():
                entrada = entrada_visita.save(commit=False)
                entrada.e_salida = "00:00"
                entrada.e_ee = Estadoentrada.objects.get(ee_estado="Pendiente⚠️")
                entrada.save()
                return redirect('cargar')

    else:
        entrada_funcionario = EntradaFuncionario()
        entrada_cobrador = EntradaCobrador()
        entrada_proveedor = EntradaProveedor()
        entrada_visita = EntradaVisita()

    return render(request, 'cargar.html', {
        'form_funcionario': entrada_funcionario,
        'form_cobrador': entrada_cobrador,
        'form_proveedor': entrada_proveedor,
        'form_visita': entrada_visita,
    })

# añadir/eliminar proveedores/cobradores
@login_required
@user_passes_test(is_swap_porteria)
def formularios(request):
    accion = request.GET.get('accion', 'agregar_cobrador')  # Valor por defecto

    if accion == 'agregar_cobrador':
        if request.method == 'POST':
            form = NewCobrador(request.POST)
            if form.is_valid():
                cobrador = form.save(commit=False)
                cobrador.cob_estado = 'activo'
                cobrador.save()
                return redirect('cargar')
        else:
            form = NewCobrador()
        
        contexto = {
            'form': form,
            'titulo': 'Añadir Cobrador',
            'texto_boton': 'Guardar',
        }

    elif accion == 'eliminar_cobrador':
        if request.method == 'POST':
            form = EliminarCobrador(request.POST)
            if form.is_valid():
                cobrador = form.cleaned_data['cobrador']
                cobrador.cob_estado = 'inactivo'
                cobrador.save()
                return redirect('cargar')
        else:
            form = EliminarCobrador()

        contexto = {
            'form': form,
            'titulo': 'Eliminar Cobrador',
            'texto_boton': 'Eliminar',
        }

    elif accion == 'agregar_proveedor':
        if request.method == 'POST':
            form = NewProveedor(request.POST)
            if form.is_valid():
                proveedor = form.save(commit=False)
                proveedor.prov_estado = 'activo'
                proveedor.save()
                return redirect('cargar')
        else:
            form = NewProveedor()
        
        contexto = {
            'form': form,
            'titulo': 'Añadir Proveedor',
            'texto_boton': 'Guardar',
        }

    elif accion == 'eliminar_proveedor':
        if request.method == 'POST':
            form = EliminarProveedor(request.POST)
            if form.is_valid():
                proveedor = form.cleaned_data['cobrador']
                proveedor.prov_estado = 'inactivo'
                proveedor.save()
                return redirect('cargar')
        else:
            form = EliminarProveedor()

        contexto = {
            'form': form,
            'titulo': 'Eliminar Proveedor',
            'texto_boton': 'Eliminar',
        }

    return render(request, "formularios.html", contexto)

# cargar salidas de todos
#[SISTEMA DE FILTRADO DE DATOS LINDO]
@login_required
@user_passes_test(is_swap_porteria)
def salida(request):
    # Solo entradas con funcionario (y sin cobrador, proveedor ni visita)
    entrada_funcionarios = Entrada.objects.filter(

        e_fun__isnull=False,
        e_prov__isnull=True,
        e_cob__isnull=True,
        e_visita__isnull=True,
        e_ee__ee_estado="Pendiente⚠️"
    )
    # Solo entradas con proveedor
    entrada_proveedores = Entrada.objects.filter(
        e_fun__isnull=True,
        e_prov__isnull=False,
        e_cob__isnull=True,
        e_visita__isnull=True,
        e_ee__ee_estado="Pendiente⚠️"
    )
    # Solo entradas con cobrador
    entrada_cobradores = Entrada.objects.filter(
        e_fun__isnull=True,
        e_prov__isnull=True,
        e_cob__isnull=False,
        e_visita__isnull=True,
        e_ee__ee_estado="Pendiente⚠️"
    )
    # Solo entradas con visita (texto)
    entrada_visitas = Entrada.objects.filter(
        e_fun__isnull=True,
        e_prov__isnull=True,
        e_cob__isnull=True,
        e_ee__ee_estado="Pendiente⚠️"
    ).exclude(e_visita__isnull=True).exclude(e_visita__exact='')
    
    estados = Estadoentrada.objects.all()
    
    return render(request, "salida.html", {
        'entrada_funcionarios': entrada_funcionarios,
        'entrada_proveedores': entrada_proveedores,
        'entrada_cobradores': entrada_cobradores,
        'entrada_visitas': entrada_visitas,
        
        'estados': estados,
    })
    
# cambiar el estado
@login_required
@user_passes_test(is_swap_porteria)
def editar_entrada(request, e_id):
    if request.method == "POST":
        entrada = get_object_or_404(Entrada, e_id=e_id)

        entrada.e_salida = request.POST.get("e_salida")
        entrada.e_comentario = request.POST.get("e_comentario")
        estado_id = request.POST.get("e_ee")

        if estado_id:
            entrada.e_ee = Estadoentrada.objects.get(pk=estado_id)

        entrada.save()
    return redirect('salida')

# ver registros guardados
@login_required
@user_passes_test(is_swap_porteria)
def ver(request):
    entradas = Entrada.objects.filter(e_ee__ee_estado="Finalizado✅")

    fecha_exacta = request.GET.get('fecha_exacta')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    funcionario_id = request.GET.get('funcionario')
    if funcionario_id:
        entradas = entradas.filter(e_fun__fun_id=funcionario_id)

    proveedor_id = request.GET.get('proveedor')
    if proveedor_id:
        entradas = entradas.filter(e_prov__prov_id=proveedor_id)

    cobrador_id = request.GET.get('cobrador')
    if cobrador_id:
        entradas = entradas.filter(e_cob__cob_id=cobrador_id)


    
    visita_texto = request.GET.get('visita')

    if fecha_exacta:
        entradas = entradas.filter(e_fecha=fecha_exacta)
    if fecha_desde:
        entradas = entradas.filter(e_fecha__gte=fecha_desde)
    if fecha_hasta:
        entradas = entradas.filter(e_fecha__lte=fecha_hasta)
    if funcionario_id:
        entradas = entradas.filter(e_fun=funcionario_id)
    if proveedor_id:
        entradas = entradas.filter(e_prov=proveedor_id)
    if cobrador_id:
        entradas = entradas.filter(e_cob=cobrador_id)
    if visita_texto:
        entradas = entradas.filter(e_visita__icontains=visita_texto)

    funcionarios = Funcionarios.objects.all()
    proveedores = Proveedor.objects.all()
    cobradores = Cobrador.objects.all()

    return render(request, "ver.html", {
        'entradas': entradas,
        'funcionarios': funcionarios,
        'proveedores': proveedores,
        'cobradores': cobradores,
    })
    
    