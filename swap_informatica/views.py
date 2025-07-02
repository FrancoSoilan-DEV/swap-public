from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.dateparse import parse_date
from django.http import HttpResponse
import openpyxl
from django.db.models.functions import ExtractMonth
from django.views.decorators.http import require_POST
from .utils import crear_mantenimiento_desde_calendario


# --- Proteger de otros Usuarios Logeados ---
def is_swap_informatica(user):
    return user.groups.filter(name='Informatica').exists()


# ==================== VISTA PRINCIPAL ====================
@login_required
@user_passes_test(is_swap_informatica)
def informatica(request):
    tarea = Tareas.objects.filter(Q(tarea_dpto__dpto_nombre="Informatica") | Q(tarea_dpto__dpto_nombre="General"))
    tarea_dia = Tareadia.objects.all()
    tarea_estado = Tareaestado.objects.exclude(te_estado__iexact="General")
    agregar_form = TareaForm()
    eliminar_form = EliminarTareaForm()

    if request.method == "POST":
        if "agregar_tarea" in request.POST:
            agregar_form = TareaForm(request.POST)  
            if agregar_form.is_valid():
                tarea = agregar_form.save(commit=False)
                departamento_informatica = Departamentos.objects.get(dpto_nombre="Informatica")
                tarea.tarea_dpto = departamento_informatica
                tarea.save()
                return redirect("informatica")
        elif "eliminar_tarea" in request.POST:
            eliminar_form = EliminarTareaForm(request.POST)
            if eliminar_form.is_valid():
                tarea = eliminar_form.cleaned_data["tarea_titulo"]
                tarea.delete()
                return redirect("informatica")

    return render(request, 'informatica.html', {
        'tarea': tarea,
        'dia': tarea_dia,
        'estado': tarea_estado,
        'agregar_form': agregar_form,
        'eliminar_form': eliminar_form,
    })

@login_required
@user_passes_test(is_swap_informatica)
def actualizar_estado(request, tarea_id):
    if request.method == "POST":
        tarea = get_object_or_404(Tareas, pk=tarea_id)
        # Obtener el nuevo estado desde el formulario
        nuevo_estado = request.POST.get("estado")
        # Buscar el estado en la base de datos
        estado_obj = get_object_or_404(Tareaestado, te_estado=nuevo_estado)
        # Actualizar la tarea con el nuevo estado
        tarea.tarea_te = estado_obj
        tarea.save()
    return redirect("informatica")  # Redirige a la misma página después de actualizar
# ==================== VISTA PRINCIPAL ====================



# ==================== BACKUPS ====================
@login_required
@user_passes_test(is_swap_informatica)
def backups(request):
    bk = Backups.objects.filter(b_estado='activo')
    bkechos = Backupshechos.objects.all()
    bkdia = Backupsdia.objects.all()
    bkestado = Backupsestado.objects.all()

    bkproceso = Backupsproceso.objects.exclude(bp_be__be_estado="Inactivo❌")

    form = BackupForm()
    form2 = BackupsProcesoForm()
    funcionarios = Funcionarios.objects.filter(fun_estado='activo')

    fce = Funcionarioconequipo.objects.filter(fce_estado='activo')
    form3 = fceForm()

    return render(request, 'backups.html', {
        'bk':bk,
        'bkechos': bkechos,
        'bkdia': bkdia,
        'bkestado':bkestado,
        'bkproceso':bkproceso,
        'form': form,
        'form2':form2,
        'funcionarios':funcionarios,
        'fce':fce,
        'form3': form3,
    })

# ACTUALIZAR ESTADO BACKUP SEMANAL
@login_required
@user_passes_test(is_swap_informatica)
def actualizar_estado_bk(request, bp_id):
    if request.method == "POST":
        bp = get_object_or_404(Backupsproceso, pk=bp_id)

        nuevo_estado = request.POST.get("bkestado")

        estado_obj = get_object_or_404(Backupsestado, be_estado=nuevo_estado)

        bp.bp_be = estado_obj
        bp.save()
    return redirect("backups")

#   AÑADIR BACKUPS SEMANALES
@login_required
@user_passes_test(is_swap_informatica)
def add_backup(request):
    if request.method == "POST":
        form = BackupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("backups")
    return redirect("backups")

# DARLE/ELIMINAR UN BACKUP A UN FUNCIONARIO CON EQUIPO
@login_required
@user_passes_test(is_swap_informatica)
def add_bk(request):
    if request.method == "POST":
        form2 = BackupsProcesoForm(request.POST)
        if form2.is_valid():
            form2.save()
            return redirect("backups")
        else:
            return redirect("backups")
    else:
        form2 = BackupsProcesoForm(request.POST)
    return redirect("backups")

@login_required
@user_passes_test(is_swap_informatica)
def delete_bk(request):
    if request.method == "POST":
        bk_id = request.POST.get("bk_id")
        bk = get_object_or_404(Backups, pk=bk_id)
        try:
            bk.b_estado = "inactivo"
            bk.save()
        except:
            return redirect("backups")
        return redirect("backups")
    return redirect("backups")
# DARLE/ELIMINAR UN BACKUP A UN FUNCIONARIO CON EQUIPO

# AÑADIR/ELIMINAR FUNCIONARIO CON EQUIPO
@login_required
@user_passes_test(is_swap_informatica)
def add_fce(request):
    if request.method == "POST":
        form3 = fceForm(request.POST, request.FILES)
        if form3.is_valid():
            form3.save()
        else:
            return redirect("backups")
    else:
        form3 = fceForm(request.POST, request.FILES)
    return redirect("backups")

@login_required
@user_passes_test(is_swap_informatica)
def delete_fce(request):
    if request.method == "POST":
        fce_id = request.POST.get("fce_id")
        fce = get_object_or_404(Funcionarioconequipo, pk=fce_id)
        try:
            fce.fce_estado = "inactivo"
            fce.save()
        except:
            return redirect("backups")
        return redirect("backups")
    return redirect("backups")

# EXXCEEEELLL
@login_required
@user_passes_test(is_swap_informatica)
def exportar_excel_backups(request):
    fecha_filtro = request.GET.get('fecha', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    backup_filtro = request.GET.get('backup', '').strip()

    if backup_filtro.isdigit():
        backup_filtro = int(backup_filtro)
    else:
        backup_filtro = None

    filtros = Q()

    if fecha_filtro:
        filtros &= Q(bh_fecha=fecha_filtro)
    else:
        if fecha_desde:
            filtros &= Q(bh_fecha__gte=parse_date(fecha_desde))
        if fecha_hasta:
            filtros &= Q(bh_fecha__lte=parse_date(fecha_hasta))

    if backup_filtro is not None:
        filtros &= Q(bh_bp__bp_b_id=backup_filtro)

    backups = Backupshechos.objects.filter(filtros).order_by('-bh_fecha')

    # Crear el Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Backups"

    # ====================
    # ESTILOS AVANZADOS
    # ====================
    from openpyxl.styles import (
        Font, Border, Side, 
        PatternFill, Alignment,
        NamedStyle
    )
    
    # Estilo para el encabezado
    header_style = NamedStyle(name="header_style")
    header_style.font = Font(
        name='Arial',
        size=12,
        bold=True,
        color="FFFFFF"  # Texto blanco
    )
    header_style.fill = PatternFill(
        start_color="4F81BD",  # Azul corporativo
        end_color="4F81BD",
        fill_type="solid"
    )
    header_style.border = Border(
        left=Side(style='medium'),
        right=Side(style='medium'),
        top=Side(style='medium'),
        bottom=Side(style='medium')
    )
    header_style.alignment = Alignment(
        horizontal='center',
        vertical='center',
        wrap_text=True
    )
    
    # Estilo para celdas de datos
    data_style = NamedStyle(name="data_style")
    data_style.font = Font(
        name='Calibri',
        size=11,
        color="000000"
    )
    data_style.border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    data_style.alignment = Alignment(
        vertical='center'
    )
    
    # Estilo alterno para filas (banding)
    alternate_style = NamedStyle(name="alternate_style")
    alternate_style.fill = PatternFill(
        start_color="DCE6F1",  # Azul muy claro
        end_color="DCE6F1",
        fill_type="solid"
    )
    alternate_style.font = Font(
        name='Calibri',
        size=11
    )
    alternate_style.border = data_style.border
    alternate_style.alignment = data_style.alignment
    
    # Añadir estilos al workbook
    wb.add_named_style(header_style)
    wb.add_named_style(data_style)
    wb.add_named_style(alternate_style)
    
    # ====================
    # ENCABEZADOS
    # ====================
    headers = ["ID", "Fecha", "Backup"]
    ws.append(headers)
    
    # Aplicar estilo a los encabezados
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.style = header_style
        # Congelar encabezados
        ws.freeze_panes = "A2"
    
    # ====================
    # DATOS
    # ====================
    for row_num, b in enumerate(backups, start=2):
        ws.cell(row=row_num, column=1, value=b.bh_id)
        ws.cell(row=row_num, column=2, 
               value=b.bh_fecha.strftime('%d/%m/%Y') if b.bh_fecha else '')
        ws.cell(row=row_num, column=3, value=str(b.bh_bp))
        
        # Aplicar estilos alternados
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=row_num, column=col)
            if row_num % 2 == 0:
                cell.style = data_style
            else:
                cell.style = alternate_style
    
    # ====================
    # FORMATO AVANZADO
    # ====================
    # Ajustar anchos de columnas con límites
    column_widths = {
        'A': 10,  # ID
        'B': 15,  # Fecha
        'C': 40   # Backup
    }
    
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width
    
    # Añadir filtros
    ws.auto_filter.ref = f"A1:C{len(backups)+1}"
    
    # Añadir formato condicional para fechas futuras (opcional)
    from openpyxl.formatting.rule import CellIsRule
    future_date_rule = CellIsRule(
        operator='lessThan',
        formula=['TODAY()'],
        stopIfTrue=True,
        font=Font(color="FF0000", italic=True)  # Rojo para fechas futuras
    )
    ws.conditional_formatting.add(f'B2:B{len(backups)+1}', future_date_rule)
    
    # Crear respuesta
    # Respuesta HTTP CORRECTA
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="backups_report.xlsx"'
    wb.save(response)
    return response

# lleva a otra pagina de backups hechos
@login_required
@user_passes_test(is_swap_informatica)
def bkhechos(request):
    # Limpiar filtros
    if 'limpiar' in request.GET:
        return redirect('bk-hechos')

    fecha_filtro = request.GET.get('fecha', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    backup_filtro = request.GET.get('backup', '').strip()

    # Validar backup
    if backup_filtro.isdigit():
        backup_filtro = int(backup_filtro)
    else:
        backup_filtro = None

    filtros = Q()

    # Si se especifica fecha exacta, tiene prioridad
    if fecha_filtro:
        filtros &= Q(bh_fecha=fecha_filtro)
    else:
        if fecha_desde:
            filtros &= Q(bh_fecha__gte=parse_date(fecha_desde))
        if fecha_hasta:
            filtros &= Q(bh_fecha__lte=parse_date(fecha_hasta))

    # Filtro por backup
    if backup_filtro is not None:
        filtros &= Q(bh_bp__bp_b_id=backup_filtro)

    bkdone = Backupshechos.objects.filter(filtros).order_by('-bh_fecha')
    backups = Backups.objects.all()

    return render(request, "bkhechos.html", {
        'bkdone': bkdone,
        'backups': backups,
        'fecha_filtro': fecha_filtro,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'backup_filtro': str(backup_filtro) if backup_filtro is not None else '',
    })

@csrf_exempt
@login_required
@user_passes_test(is_swap_informatica)
def eliminar_backups(request):
    if request.method == "POST":
        delete_ids = request.POST.getlist('delete_ids')
        if delete_ids:
            Backupshechos.objects.filter(bh_id__in=delete_ids).delete()
    return redirect('bk-hechos')

# ayuda a agregar los backupshechos
#@login_required
#@user_passes_test(is_swap_informatica)
# Los decoradores @login_required y @user_passes_test solo deben usarse 
# en vistas (funciones que reciben request). Tu función obtener_fecha_del_dia() e
# s una función utilitaria, no una vista, y no tiene ni necesita acceso a request.
def obtener_fecha_del_dia(dia_nombre, referencia):
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    dia_actual = referencia.weekday()  # 0 = Lunes, 4 = Viernes
    dia_objetivo = dias_semana.index(dia_nombre)

    # Calcular la diferencia de días
    if dia_objetivo <= dia_actual:
        diferencia = dia_objetivo - dia_actual
    else:
        diferencia = dia_objetivo - dia_actual - 7

    return referencia + timedelta(days=diferencia)

# Se agregan los backups hechos (configuracion de horario para apretar el boton)
@user_passes_test(is_swap_informatica)
@login_required
def agregar_backups_hechos(request):
    fecha_actual = now()
    dia_actual = fecha_actual.strftime("%A")
    hora_actual = fecha_actual.strftime("%H:%M")

    # Verificar si está entre el horario permitido
    if (dia_actual == "Friday" and hora_actual >= "15:00") or dia_actual in ["Saturday", "Sunday"]:
        estado_finalizado = Backupsestado.objects.filter(be_estado="Finalizado✅").first()
        estado_pendiente = Backupsestado.objects.filter(be_estado="Pendiente⚠️").first()

        if estado_finalizado and estado_pendiente:
            procesos_finalizados = Backupsproceso.objects.filter(bp_be=estado_finalizado)

            if procesos_finalizados.exists():
                for proceso in procesos_finalizados:
                    backup_dia = proceso.bp_bd.bd_dia  # "Lunes", "Martes", etc.
                    fecha_backup = obtener_fecha_del_dia(backup_dia, fecha_actual.date())

                    # Guardar el backup hecho
                    Backupshechos.objects.create(
                        bh_fecha=fecha_backup,
                        bh_bp=proceso
                    )

                    # Cambiar el estado a "Pendiente⚠️"
                    proceso.bp_be = estado_pendiente
                    proceso.save()

    return redirect("backups")
# ==================== BACKUPS ====================



# ==================== INVENTARIO ====================
# INVENTARIO
@login_required
@user_passes_test(is_swap_informatica)
def inventario(request):
    inventario_informatica = Inventarioinformatica.objects.all()
    form = rakForm()
    form2 = StatusForm()
    form3 = ItemForm()
    form4 = NewArticleForm()


    # Obtener listas para los filtros
    categorias = InventarioinformaticaCategoria.objects.all()
    depositos = InventarioinformaticaDeposito.objects.all()
    estados = InventarioinformaticaEstado.objects.all()

    # Obtener parámetros del filtro
    articulo_filtro = request.GET.get('articulo', '').strip()
    deposito_filtro = request.GET.get('deposito', '').strip()
    estado_filtro = request.GET.get('estado', '').strip()

    # Aplicar filtros
    filtros = Q()
    if articulo_filtro:
        filtros &= Q(ii_iic_id=articulo_filtro)
    if deposito_filtro:
        filtros &= Q(ii_iid_id=deposito_filtro)
    if estado_filtro:
        filtros &= Q(ii_iie_id=estado_filtro)

    inventario_informatica = Inventarioinformatica.objects.filter(filtros)

    # datos para las ultimas 3 tablas
    items = InventarioinformaticaCategoria.objects.all()
    raks = InventarioinformaticaDeposito.objects.all()
    status = InventarioinformaticaEstado.objects.all()

    return render(request, "inventario.html", {
        'inventario_informatica': inventario_informatica,
        'form':form,
        'form2':form2,
        'form3': form3,
        'form4': form4,

        'categorias': categorias,
        'depositos': depositos,
        'estados': estados,
        'articulo_filtro': articulo_filtro,
        'deposito_filtro': deposito_filtro,
        'estado_filtro': estado_filtro,

        'items': items,
        'raks': raks,
        'status': status,
    })

# se añaden raks o depositos para inventario
@login_required
@user_passes_test(is_swap_informatica)
def agregar_rak(request):
    if request.method == "POST":
        form = rakForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventario")
    else:
        form = rakForm()  # Instancia vacía si es GET
    return redirect("inventario")

# se añaden estados para inventario
@login_required
@user_passes_test(is_swap_informatica)
def agregar_status(request):
    if request.method == "POST":
        form2 = StatusForm(request.POST)
        if form2.is_valid():
            form2.save()
            return redirect("inventario")
    else:
        form2 = StatusForm()  # Instancia vacía si es GET
    return redirect("inventario")

# se añade un item
@login_required
@user_passes_test(is_swap_informatica)
def agregar_item(request):
    if request.method == "POST":
        form3 = ItemForm(request.POST)
        if form3.is_valid():
            form3.save()
            return redirect("inventario")
    else:
        form3 = ItemForm()  # Instancia vacía si es GET
    return redirect("inventario")

# se añade un nuevo articulo
@login_required
@user_passes_test(is_swap_informatica)
def agregar_articulo(request):
    if request.method == "POST":
        form4 = NewArticleForm(request.POST)
        if form4.is_valid():
            article = form4.save(commit=False)  # No guardamos aún en la BD
            article.ii_fecha = now().date()  # Asignamos la fecha actual
            article.save()  # Guardamos en la BD
            return redirect("inventario")
    else:
        form4 = NewArticleForm()

    return redirect("inventario")

# se edita un articulo
@csrf_exempt
@login_required
@user_passes_test(is_swap_informatica)
def guardar_cantidad(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            item = Inventarioinformatica.objects.get(ii_id=data["id"])
            item.ii_cantidad = data["cantidad"]
            item.ii_fecha = timezone.now().date()  # 👈 actualizar la fecha
            item.save()
            return JsonResponse({"status": "success"})
        except Inventarioinformatica.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Artículo no encontrado"})
        
# Equipos
@login_required
@user_passes_test(is_swap_informatica)
def equipos(request):
    # Tabla General de Vistas
    equipos = Equipos.objects.select_related('eq_tipe').filter(
    Q(eq_tipe__tipe_nombre='PC') | Q(eq_tipe__tipe_nombre='Notebook'))
    
    upss = Equipos.objects.select_related('eq_tipe').filter(
    eq_tipe__tipe_nombre='UPS')
    
    impresoras = Equipos.objects.select_related('eq_tipe').filter(
        eq_tipe__tipe_nombre='Impresora')
    
    otros = Equipos.objects.select_related('eq_tipe').filter(
        Q(eq_tipe__tipe_nombre='Router') | Q(eq_tipe__tipe_nombre='DVR') | 
        Q(eq_tipe__tipe_nombre='Laser') | Q(eq_tipe__tipe_nombre='Scaner')
    )
    
    cosas_servidores = Equipos.objects.select_related('eq_tipe').filter(
        Q(eq_tipe__tipe_nombre__icontains='switch') |
        Q(eq_tipe__tipe_nombre__icontains='rack') |
        Q(eq_tipe__tipe_nombre__icontains='servidor')
    )
    
    monitores = Equipos.objects.select_related('eq_tipe').filter(
    eq_tipe__tipe_nombre='Monitor')
    
    # Tabla de Vistas de Mantenimientos
    # ===============================================================================================
    mantenimientos_equipos = Mantenimiento.objects.filter(
    Q(m_eq__eq_tipe__tipe_nombre="PC") | Q(m_eq__eq_tipe__tipe_nombre="Notebook")
    )
    
    # Filtros de mantenimientos
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    fecha_exacta = request.GET.get('fecha_exacta')
    tipo_mantenimiento = request.GET.get('tipo_mantenimiento')
    responsable = request.GET.get('responsable')
    equipo_id = request.GET.get('equipo_id')

    if fecha_exacta:
        mantenimientos_equipos = mantenimientos_equipos.filter(m_fecha=fecha_exacta)
    else:
        if fecha_desde:
            mantenimientos_equipos = mantenimientos_equipos.filter(m_fecha__gte=fecha_desde)
        if fecha_hasta:
            mantenimientos_equipos = mantenimientos_equipos.filter(m_fecha__lte=fecha_hasta)

    if tipo_mantenimiento:
        mantenimientos_equipos = mantenimientos_equipos.filter(m_mt__mt_nombre__iexact=tipo_mantenimiento)

    if responsable:
        mantenimientos_equipos = mantenimientos_equipos.filter(m_responsable__icontains=responsable)

    if equipo_id:
        mantenimientos_equipos = mantenimientos_equipos.filter(m_eq__eq_id=equipo_id)

    # ===============================================================================================
    
    mantenimientos_ups = Mantenimiento.objects.filter(
        m_eq__eq_tipe__tipe_nombre="UPS"
    )
    
    # Filtros para mantenimientos de UPS
    fecha_desde_ups = request.GET.get('fecha_desde_ups')
    fecha_hasta_ups = request.GET.get('fecha_hasta_ups')
    fecha_exacta_ups = request.GET.get('fecha_exacta_ups')
    tipo_mantenimiento_ups = request.GET.get('tipo_mantenimiento_ups')
    responsable_ups = request.GET.get('responsable_ups')
    equipo_id_ups = request.GET.get('equipo_id_ups')

    if fecha_exacta_ups:
        mantenimientos_ups = mantenimientos_ups.filter(m_fecha=fecha_exacta_ups)
    else:
        if fecha_desde_ups:
            mantenimientos_ups = mantenimientos_ups.filter(m_fecha__gte=fecha_desde_ups)
        if fecha_hasta_ups:
            mantenimientos_ups = mantenimientos_ups.filter(m_fecha__lte=fecha_hasta_ups)

    if tipo_mantenimiento_ups:
        mantenimientos_ups = mantenimientos_ups.filter(m_mt__mt_nombre__iexact=tipo_mantenimiento_ups)

    if responsable_ups:
        mantenimientos_ups = mantenimientos_ups.filter(m_responsable__icontains=responsable_ups)

    if equipo_id_ups:
        mantenimientos_ups = mantenimientos_ups.filter(m_eq__eq_id=equipo_id_ups)

    
    # ===============================================================================================
    
    mantenimientos_impresoras = Mantenimiento.objects.filter(
        m_eq__eq_tipe__tipe_nombre="Impresora"
    )
    
    # Filtros para mantenimientos de impresoras
    fecha_desde_imp = request.GET.get('fecha_desde_imp')
    fecha_hasta_imp = request.GET.get('fecha_hasta_imp')
    fecha_exacta_imp = request.GET.get('fecha_exacta_imp')
    tipo_mantenimiento_imp = request.GET.get('tipo_mantenimiento_imp')
    responsable_imp = request.GET.get('responsable_imp')
    equipo_id_imp = request.GET.get('equipo_id_imp')

    if fecha_exacta_imp:
        mantenimientos_impresoras = mantenimientos_impresoras.filter(m_fecha=fecha_exacta_imp)
    else:
        if fecha_desde_imp:
            mantenimientos_impresoras = mantenimientos_impresoras.filter(m_fecha__gte=fecha_desde_imp)
        if fecha_hasta_imp:
            mantenimientos_impresoras = mantenimientos_impresoras.filter(m_fecha__lte=fecha_hasta_imp)

    if tipo_mantenimiento_imp:
        mantenimientos_impresoras = mantenimientos_impresoras.filter(m_mt__mt_nombre__iexact=tipo_mantenimiento_imp)

    if responsable_imp:
        mantenimientos_impresoras = mantenimientos_impresoras.filter(m_responsable__icontains=responsable_imp)

    if equipo_id_imp:
        mantenimientos_impresoras = mantenimientos_impresoras.filter(m_eq__eq_id=equipo_id_imp)

    
    # ===============================================================================================
    
    mantenimientos_otros = Mantenimiento.objects.filter(
    Q(m_eq__eq_tipe__tipe_nombre__icontains="router") | Q(m_eq__eq_tipe__tipe_nombre__icontains="DVR") |
    Q(m_eq__eq_tipe__tipe_nombre__icontains="laser") | Q(m_eq__eq_tipe__tipe_nombre__icontains="Scaner")
    )
    
    # Filtros para mantenimientos de otros dispositivos
    fecha_desde_otros = request.GET.get('fecha_desde_otros')
    fecha_hasta_otros = request.GET.get('fecha_hasta_otros')
    fecha_exacta_otros = request.GET.get('fecha_exacta_otros')
    tipo_mantenimiento_otros = request.GET.get('tipo_mantenimiento_otros')
    responsable_otros = request.GET.get('responsable_otros')
    equipo_id_otros = request.GET.get('equipo_id_otros')

    if fecha_exacta_otros:
        mantenimientos_otros = mantenimientos_otros.filter(m_fecha=fecha_exacta_otros)
    else:
        if fecha_desde_otros:
            mantenimientos_otros = mantenimientos_otros.filter(m_fecha__gte=fecha_desde_otros)
        if fecha_hasta_otros:
            mantenimientos_otros = mantenimientos_otros.filter(m_fecha__lte=fecha_hasta_otros)

    if tipo_mantenimiento_otros:
        mantenimientos_otros = mantenimientos_otros.filter(m_mt__mt_nombre__iexact=tipo_mantenimiento_otros)

    if responsable_otros:
        mantenimientos_otros = mantenimientos_otros.filter(m_responsable__icontains=responsable_otros)

    if equipo_id_otros:
        mantenimientos_otros = mantenimientos_otros.filter(m_eq__eq_id=equipo_id_otros)

    
    # ===============================================================================================
    
    mantenimientos_servidores = Mantenimiento.objects.filter(
        Q(m_eq__eq_tipe__tipe_nombre__icontains="switch") | Q(m_eq__eq_tipe__tipe_nombre__icontains="rack") |
        Q(m_eq__eq_tipe__tipe_nombre__icontains="servidor")
    )

    # Filtros para mantenimientos de servidores
    fecha_desde_srv = request.GET.get('fecha_desde_srv')
    fecha_hasta_srv = request.GET.get('fecha_hasta_srv')
    fecha_exacta_srv = request.GET.get('fecha_exacta_srv')
    tipo_mantenimiento_srv = request.GET.get('tipo_mantenimiento_srv')
    responsable_srv = request.GET.get('responsable_srv')
    equipo_id_srv = request.GET.get('equipo_id_srv')

    if fecha_exacta_srv:
        mantenimientos_servidores = mantenimientos_servidores.filter(m_fecha=fecha_exacta_srv)
    else:
        if fecha_desde_srv:
            mantenimientos_servidores = mantenimientos_servidores.filter(m_fecha__gte=fecha_desde_srv)
        if fecha_hasta_srv:
            mantenimientos_servidores = mantenimientos_servidores.filter(m_fecha__lte=fecha_hasta_srv)

    if tipo_mantenimiento_srv:
        mantenimientos_servidores = mantenimientos_servidores.filter(m_mt__mt_nombre__iexact=tipo_mantenimiento_srv)

    if responsable_srv:
        mantenimientos_servidores = mantenimientos_servidores.filter(m_responsable__icontains=responsable_srv)

    if equipo_id_srv:
        mantenimientos_servidores = mantenimientos_servidores.filter(m_eq__eq_id=equipo_id_srv)

    

    # Filtros para cosas de servidores
    tipo_equipo_servidor = request.GET.get('tipo_equipo_servidor')
    departamento_servidor = request.GET.get('departamento_servidor')
    usuario_servidor = request.GET.get('usuario_servidor')

    cosas_servidores = Equipos.objects.select_related('eq_tipe')

    # Filtrar por tipo
    if tipo_equipo_servidor:
        cosas_servidores = cosas_servidores.filter(eq_tipe__tipe_nombre__iexact=tipo_equipo_servidor)
    else:
        cosas_servidores = cosas_servidores.filter(
            Q(eq_tipe__tipe_nombre__icontains='switch') |
            Q(eq_tipe__tipe_nombre__icontains='rack') |
            Q(eq_tipe__tipe_nombre__icontains='servidor')
        )

    # Filtrar por departamento
    if departamento_servidor:
        cosas_servidores = cosas_servidores.filter(eq_dpto=departamento_servidor)

    # Filtrar por usuario
    if usuario_servidor:
        cosas_servidores = cosas_servidores.filter(eq_usuario__icontains=usuario_servidor)


    # ===============================================================================================

    mantenimientos_monitores = Mantenimiento.objects.filter(
        m_eq__eq_tipe__tipe_nombre__icontains="monitor"
    )
    
    # Filtros para mantenimientos de monitores
    fecha_desde_monitor = request.GET.get('fecha_desde_monitor')
    fecha_hasta_monitor = request.GET.get('fecha_hasta_monitor')
    fecha_exacta_monitor = request.GET.get('fecha_exacta_monitor')
    tipo_mantenimiento_monitor = request.GET.get('tipo_mantenimiento_monitor')
    responsable_monitor = request.GET.get('responsable_monitor')
    equipo_id_monitor = request.GET.get('equipo_id_monitor')

    if fecha_exacta_monitor:
        mantenimientos_monitores = mantenimientos_monitores.filter(m_fecha=fecha_exacta_monitor)
    else:
        if fecha_desde_monitor:
            mantenimientos_monitores = mantenimientos_monitores.filter(m_fecha__gte=fecha_desde_monitor)
        if fecha_hasta_monitor:
            mantenimientos_monitores = mantenimientos_monitores.filter(m_fecha__lte=fecha_hasta_monitor)

    if tipo_mantenimiento_monitor:
        mantenimientos_monitores = mantenimientos_monitores.filter(m_mt__mt_nombre__iexact=tipo_mantenimiento_monitor)

    if responsable_monitor:
        mantenimientos_monitores = mantenimientos_monitores.filter(m_responsable__icontains=responsable_monitor)

    if equipo_id_monitor:
        mantenimientos_monitores = mantenimientos_monitores.filter(m_eq__eq_id=equipo_id_monitor)

    
    # ===============================================================================================
    
    # filtro equipos
    tipo_equipo = request.GET.get('tipo_equipo')
    departamento = request.GET.get('departamento')
    usuario = request.GET.get('usuario')
    departamentos = Departamentos.objects.all()
    if tipo_equipo:
        equipos = equipos.filter(eq_tipe__tipe_nombre__iexact=tipo_equipo)
    
    if departamento:
        equipos = equipos.filter(eq_dpto__dpto_id=departamento)

    if usuario:
        equipos = equipos.filter(responsable__icontains=usuario)
    
    # filtro ups's
    if departamento:
        upss = upss.filter(eq_dpto__dpto_id=departamento)
        
    if usuario:
        upss = upss.filter(responsable__icontains=usuario)#

    # filtro impresoras
    if departamento:
        impresoras = impresoras.filter(eq_dpto__dpto_id=departamento)

    if usuario:
        impresoras = impresoras.filter(responsable__icontains=usuario)
        
    # filtro otros
    tipo_equipo_otros = request.GET.get('tipo_equipo_otros')
    departamento_otros = request.GET.get('departamento_otros')
    usuario_otros = request.GET.get('usuario_otros')

    if tipo_equipo_otros:
        otros = otros.filter(eq_tipe__tipe_nombre__iexact=tipo_equipo_otros)

    if departamento_otros:
        otros = otros.filter(eq_dpto__dpto_id=departamento_otros)

    if usuario_otros:
        otros = otros.filter(responsable=usuario_otros)
        
    # filtro cosas_servidores
    tipo_equipo = request.GET.get('tipo_equipo_servidor')

    if tipo_equipo:
        if tipo_equipo == 'servidor':
            cosas_servidores = cosas_servidores.filter(eq_tipe__tipe_nombre__icontains='servidor')
        else:
            cosas_servidores = cosas_servidores.filter(eq_tipe__tipe_nombre__iexact=tipo_equipo)

    # filtro monitores
    departamento_monitor = request.GET.get('departamento_monitor')
    usuario_monitor = request.GET.get('usuario_monitor')

    if departamento_monitor:
        monitores = monitores.filter(eq_dpto__dpto_id=departamento_monitor)

    if usuario_monitor:
        monitores = monitores.filter(responsable=usuario_monitor)

        
    return render(request, "equipos.html",{
        'equipos': equipos,
        'upss': upss,
        'impresoras': impresoras,
        'otros': otros,
        'cosas_servidores': cosas_servidores,
        'monitores': monitores,
        
        'mantenimientos_equipos':mantenimientos_equipos,
        'mantenimientos_ups':mantenimientos_ups,
        'mantenimientos_impresoras':mantenimientos_impresoras,
        'mantenimientos_otros':mantenimientos_otros,
        'mantenimientos_servidores':mantenimientos_servidores,
        'mantenimientos_monitores':mantenimientos_monitores,
        
        # NUEVO: enviar departamentos para el filtro
        'departamentos': departamentos,
    })
    
# AÑADIR EQUIPOS
@login_required
@user_passes_test(is_swap_informatica)
def NuevoEquipo(request):
    form_type = request.GET.get('form', 'equipo')  # por defecto equipo

    # Diccionario para mapear los tipos a los formularios
    form_classes = {
        'equipo': NewEquipo,
        'ups': NewUps,
        'impresora': NewImpresora,
        'otros': NewOtros,
        'servidor': NewCosasServidor,
        'monitor': NewMonitor,
    }

    FormClass = form_classes.get(form_type)

    if FormClass is None:
        return render(request, '404.html')  # o redirigir a una página de error personalizada

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipos')  # cambialo por la URL que tengas
    else:
        form = FormClass()

    return render(request, 'add.html', {'form': form, 'form_type': form_type})
# ==================== INVENTARIO ====================



# ========== MANTENIMIENTO ====================
# MANTENIMIENTO
from django.db.models.functions import ExtractMonth

@login_required
@user_passes_test(is_swap_informatica)
def mantenimiento(request):
    mantenimientos_enero = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=1).order_by('mc_fecha')
    
    mantenimientos_febrero = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=2).order_by('mc_fecha')
    
    mantenimientos_marzo = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=3).order_by('mc_fecha')
    
    mantenimientos_abril = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=4).order_by('mc_fecha')
    
    mantenimientos_mayo = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=5).order_by('mc_fecha')
    
    mantenimientos_junio = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=6).order_by('mc_fecha')
    
    mantenimientos_julio = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=7).order_by('mc_fecha')
    
    mantenimientos_agosto = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=8).order_by('mc_fecha')
    
    mantenimientos_septiembre = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=9).order_by('mc_fecha')
    
    mantenimientos_octubre = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=10).order_by('mc_fecha')
    
    mantenimientos_noviembre = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=11).order_by('mc_fecha')
    
    mantenimientos_diciembre = Mantenimientocalendario.objects.annotate(
        mes=ExtractMonth('mc_fecha')).filter(mes=12).order_by('mc_fecha')
    
    return render(request, "mantenimiento.html", {
        'mantenimientos_enero': mantenimientos_enero,
        'mantenimientos_febrero': mantenimientos_febrero,
        'mantenimientos_marzo': mantenimientos_marzo,
        'mantenimientos_abril': mantenimientos_abril,
        'mantenimientos_mayo': mantenimientos_mayo,
        'mantenimientos_junio': mantenimientos_junio,
        'mantenimientos_julio': mantenimientos_julio,
        'mantenimientos_agosto': mantenimientos_agosto,
        'mantenimientos_septiembre': mantenimientos_septiembre,
        'mantenimientos_octubre': mantenimientos_octubre,
        'mantenimientos_noviembre': mantenimientos_noviembre,
        'mantenimientos_diciembre': mantenimientos_diciembre,
    })


@require_POST
@login_required
@user_passes_test(is_swap_informatica)
def cambiar_estado_mantenimiento(request, mc_id):
    nuevo_estado = request.POST.get('estado')
    responsable = request.POST.get('responsable')  # viene vacío si no es finalizado

    mantenimiento = get_object_or_404(Mantenimientocalendario, mc_id=mc_id)

    estado_obj, _ = Mantenimientoestado.objects.get_or_create(me_estado=nuevo_estado)
    mantenimiento.mc_me = estado_obj
    mantenimiento.save()

    if nuevo_estado == "Finalizado✅" and responsable:
        crear_mantenimiento_desde_calendario(mantenimiento, responsable)

    return redirect('mantenimiento')

@login_required
@user_passes_test(is_swap_informatica)
def addmantenimiento(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addmantenimiento')  # Redirige a donde necesites
    else:
        form = MantenimientoForm()
    return render(request, 'addmantenimiento.html',{
        'form':form,
    })

# ========== MANTENIMIENTO ====================

# bk = Backups.objects.filter(b_estado='activo')