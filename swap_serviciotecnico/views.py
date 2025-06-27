from django.shortcuts import render, redirect
from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta,datetime
from django.db.models import Count
from calendar import month_name
import openpyxl
from openpyxl.styles import (
    Font, PatternFill, Border, Side, Alignment,
    NamedStyle, numbers
)
from django.http import HttpResponse
from openpyxl.styles import GradientFill

# Create your views here.

# --- Proteger de otros Usuarios Logeados ---
def is_swap_serviciotecnico(user):
    return user.groups.filter(name='ServicioTecnico').exists()

# menu principal servicio tecnico
@login_required
@user_passes_test(is_swap_serviciotecnico)
def serviciotecnico(request):
    tarea = Tareas.objects.filter(tarea_dpto__dpto_nombre="General")
    tarea_dia = Tareadia.objects.filter(td_dia="General")
    
    return render(request, "serviciotecnico.html",{
        'tarea': tarea,
        'dia': tarea_dia,
    })
    
# ver los registros ingresados por los trabajodores
@login_required
@user_passes_test(is_swap_serviciotecnico)
def veregistro(request):
    trabajos_realizados = Tecnicos.objects.filter(tec_ee__ee_estado="Pendiente⚠️")

    funcionario = request.GET.get("funcionario")
    fecha_exacta = request.GET.get("fecha_exacta")
    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")

    if funcionario:
        trabajos_realizados = trabajos_realizados.filter(tec_nombre__icontains=funcionario)

    if fecha_exacta:
        trabajos_realizados = trabajos_realizados.filter(tec_fecha=fecha_exacta)

    if fecha_desde:
        trabajos_realizados = trabajos_realizados.filter(tec_fecha__gte=fecha_desde)

    if fecha_hasta:
        trabajos_realizados = trabajos_realizados.filter(tec_fecha__lte=fecha_hasta)

    # Traer nombres únicos de técnicos desde Tecnicos (asegurando que no se repitan)
    lista_tecnicos = (
        Tecnicos.objects.order_by("tec_nombre")
        .values_list("tec_nombre", flat=True)
        .distinct()
    )

    lista_estados = Estadoentrada.objects.all()
    lista_montos = Tecnicosmonto.objects.all()

    return render(request, "veregistros.html", {
        'trabajos_realizados': trabajos_realizados,
        'lista_tecnicos': lista_tecnicos,
        'lista_estados': lista_estados,
        'lista_montos': lista_montos,
    })



from django.shortcuts import redirect, get_object_or_404
# se realiza cambios correspondientes (estados u monto)
@login_required
@user_passes_test(is_swap_serviciotecnico)
def editar_trabajo(request, tec_id):
    if request.method == 'POST':
        trabajo = get_object_or_404(Tecnicos, pk=tec_id)
        nuevo_estado_id = request.POST.get('estado')
        nuevo_monto_id = request.POST.get('monto')

        if nuevo_estado_id:
            trabajo.tec_ee_id = nuevo_estado_id
        if nuevo_monto_id:
            trabajo.tec_tm_id = nuevo_monto_id
        trabajo.save()

    return redirect('veregistro')

# se añade nuevo monto
@login_required
@user_passes_test(is_swap_serviciotecnico)
def addmonto(request):
    if request.method == 'POST':
        form = MontoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addmonto')  # Redirige a donde necesites
    else:
        form = MontoForm()
    return render(request,"addmonto.html",{
        'form':form,
    })


# se ve el historial de todos los trabajos
@login_required
@user_passes_test(is_swap_serviciotecnico)
def historial(request):
    # Obtener parámetros de filtro
    filtro_tipo = request.GET.get('filtro_tipo', '30_dias')  # Por defecto: últimos 30 días
    mes_inicio = request.GET.get('mes_inicio')
    mes_fin = request.GET.get('mes_fin')
    año_inicio = request.GET.get('año_inicio')
    año_fin = request.GET.get('año_fin')
    mes_exacto = request.GET.get('mes_exacto')
    año_exacto = request.GET.get('año_exacto')

    # Consulta base
    datos_query = Tecnicos.objects.filter(tec_ee__ee_estado='Finalizado✅')

    # Preparar datos según el tipo de filtro
    if filtro_tipo == 'rango_meses':
        # Filtro por rango de meses (suma por mes)
        datos = (
            datos_query
            .filter(tec_fecha__month__gte=mes_inicio, tec_fecha__month__lte=mes_fin)
            .filter(tec_fecha__year__gte=año_inicio, tec_fecha__year__lte=año_fin)
            .values('tec_fecha__year', 'tec_fecha__month')
            .annotate(total=Count('tec_id'))
            .order_by('tec_fecha__year', 'tec_fecha__month')
        )
        labels = [f"{month_name[d['tec_fecha__month']]} {d['tec_fecha__year']}" for d in datos]

        valores = [d['total'] for d in datos]
        
    elif filtro_tipo == 'mes_exacto':
        # Filtro por mes exacto (días completos)
        year = int(año_exacto)
        month = int(mes_exacto)
        
        # Generar todos los días del mes
        num_days = (datetime(year=year, month=month+1, day=1) - 
                   datetime(year=year, month=month, day=1)).days if month != 12 else 31
        
        # Consulta para el mes seleccionado
        datos_db = (
            datos_query
            .filter(tec_fecha__year=year, tec_fecha__month=month)
            .values('tec_fecha__day')
            .annotate(total=Count('tec_id'))
            .order_by('tec_fecha__day')
        )
        
        # Convertir a diccionario para fácil acceso
        datos_dict = {d['tec_fecha__day']: d['total'] for d in datos_db}
        
        # Crear datos completos (incluyendo días sin registros)
        labels = []
        valores = []
        for day in range(1, num_days+1):
            labels.append(f"{day}/{month}/{year}")
            valores.append(datos_dict.get(day, 0))
            
    elif filtro_tipo == 'rango_años':
        # Filtro por rango de años (suma por año)
        datos = (
            datos_query
            .filter(tec_fecha__year__gte=año_inicio, tec_fecha__year__lte=año_fin)
            .values('tec_fecha__year')
            .annotate(total=Count('tec_id'))
            .order_by('tec_fecha__year')
        )
        labels = [str(d['tec_fecha__year']) for d in datos]
        valores = [d['total'] for d in datos]
        
    else:  # Por defecto: últimos 30 días
        fecha_limite = timezone.now().date() - timedelta(days=30)
        
        # Generar rango de fechas de los últimos 30 días
        date_range = [fecha_limite + timedelta(days=x) for x in range(31)]
        
        # Consulta para los últimos 30 días
        datos_db = (
            datos_query
            .filter(tec_fecha__gte=fecha_limite)
            .values('tec_fecha')
            .annotate(total=Count('tec_id'))
            .order_by('tec_fecha')
        )
        
        # Convertir a diccionario para fácil acceso
        datos_dict = {d['tec_fecha']: d['total'] for d in datos_db}
        
        # Crear datos completos (incluyendo días sin registros)
        labels = []
        valores = []
        for date in date_range:
            labels.append(date.strftime('%d/%m/%Y'))
            valores.append(datos_dict.get(date, 0))

    # Obtener años y meses disponibles para los filtros
    años_disponibles = (
        datos_query
        .dates('tec_fecha', 'year')
        .order_by('-tec_fecha__year')
    )
    
    meses_disponibles = [
        {'num': i, 'nombre': month_name[i]} 
        for i in range(1, 13)
    ]




    trabajos_realizados = Tecnicos.objects.all()
    funcionario = request.GET.get("funcionario")
    fecha_exacta = request.GET.get("fecha_exacta")
    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")
    estado = request.GET.get("estado")  # Nuevo filtro
    
    if funcionario:
        trabajos_realizados = trabajos_realizados.filter(tec_nombre__icontains=funcionario)

    if fecha_exacta:
        trabajos_realizados = trabajos_realizados.filter(tec_fecha=fecha_exacta)

    if fecha_desde:
        trabajos_realizados = trabajos_realizados.filter(tec_fecha__gte=fecha_desde)

    if fecha_hasta:
        trabajos_realizados = trabajos_realizados.filter(tec_fecha__lte=fecha_hasta)
    if estado:
        trabajos_realizados = trabajos_realizados.filter(tec_ee__ee_estado=estado)  # o usar `tec_ee__ee_id=estado` si pasas el ID
    lista_tecnicos = (
        Tecnicos.objects.order_by("tec_nombre")
        .values_list("tec_nombre", flat=True)
        .distinct()
    )

    lista_estados = Estadoentrada.objects.all()
    lista_montos = Tecnicosmonto.objects.all()
    return render(request, 'historial.html', {
        'labels': labels,
        'datos': valores,
        'años_disponibles': años_disponibles,
        'meses_disponibles': meses_disponibles,
        'filtro_actual': filtro_tipo,
        
        'trabajos_realizados': trabajos_realizados,
        'lista_tecnicos': lista_tecnicos,
        'lista_estados': lista_estados,
        'lista_montos': lista_montos,
    })
    
    
    

# excel
@login_required
@user_passes_test(is_swap_serviciotecnico)
def e_e(request):
    # Filtrar los datos
    trabajos = Tecnicos.objects.all()

    funcionario = request.GET.get("funcionario")
    fecha_exacta = request.GET.get("fecha_exacta")
    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")
    estado = request.GET.get("estado")

    if funcionario:
        trabajos_realizados = trabajos_realizados.filter(tec_nombre__icontains=funcionario)
    if fecha_exacta:
        trabajos = trabajos.filter(tec_fecha=fecha_exacta)
    if fecha_desde:
        trabajos = trabajos.filter(tec_fecha__gte=fecha_desde)
    if fecha_hasta:
        trabajos = trabajos.filter(tec_fecha__lte=fecha_hasta)
    if estado:
        trabajos = trabajos.filter(tec_ee__ee_estado=estado)

    # Crear libro Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Trabajos Realizados"

    # =============================================
    # PALETA DE COLORES AZULES MODERNOS
    # =============================================
    AZUL_OSCURO = "2E5C8A"       # Azul marino
    AZUL_MEDIO = "4361EE"        # Azul vibrante
    AZUL_CLARO = "4CC9F0"        # Azul cielo
    AZUL_GRADIENTE_INICIO = "3A0CA3"  # Para gradiente
    AZUL_GRADIENTE_FIN = "4895EF"     # Para gradiente
    GRIS_CLARO = "F5F7FA"        # Fondo claro
    GRIS_MEDIO = "E0E5EC"        # Para bordes
    BLANCO = "FFFFFF"
    TEXTO_OSCURO = "2B2D42"

    # =============================================
    # ESTILOS MEJORADOS
    # =============================================
    
    # Estilo para el encabezado con gradiente azul
    header_style = NamedStyle(name="header_style")
    header_style.font = Font(bold=True, color=BLANCO, size=12, name='Segoe UI')
    header_style.fill = GradientFill(
        stop=(AZUL_GRADIENTE_INICIO, AZUL_GRADIENTE_FIN),
        type="linear",
        degree=45
    )
    header_style.border = Border(
        bottom=Side(border_style="medium", color=AZUL_OSCURO),
        left=Side(border_style="thin", color=AZUL_MEDIO + "80"),  # 50% opacity
        right=Side(border_style="thin", color=AZUL_MEDIO + "80"),
        top=Side(border_style="medium", color=AZUL_OSCURO)
    )
    header_style.alignment = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True
    )
    
    # Estilo para datos normales (todos iguales, incluido estado)
    data_style = NamedStyle(name="data_style")
    data_style.font = Font(size=11, name='Segoe UI', color=TEXTO_OSCURO)
    data_style.border = Border(
        bottom=Side(border_style="thin", color=GRIS_MEDIO),
        left=Side(border_style="thin", color=GRIS_MEDIO),
        right=Side(border_style="thin", color=GRIS_MEDIO),
        top=Side(border_style="thin", color=GRIS_MEDIO)
    )
    data_style.alignment = Alignment(
        vertical="center",
        wrap_text=True
    )
    
    # Estilo para filas pares
    even_row_style = NamedStyle(name="even_row_style")
    even_row_style.fill = PatternFill(
        start_color=BLANCO,
        end_color=BLANCO,
        fill_type="solid"
    )
    
    # Estilo para filas impares
    odd_row_style = NamedStyle(name="odd_row_style")
    odd_row_style.fill = PatternFill(
        start_color=GRIS_CLARO,
        end_color=GRIS_CLARO,
        fill_type="solid"
    )
    
    # Estilo para montos
    money_style = NamedStyle(name="money_style")
    money_style.number_format = '#,##0" Gs"'
    money_style.font = Font(size=11, name='Segoe UI', color=TEXTO_OSCURO)
    money_style.alignment = Alignment(
        horizontal="right",
        vertical="center"
    )
    
    # Estilo para fechas (solo fecha)
    date_style = NamedStyle(name="date_style")
    date_style.number_format = 'DD/MM/YYYY'
    date_style.font = Font(size=11, name='Segoe UI', color=TEXTO_OSCURO)
    date_style.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )
    
    # Estilo para horas (formato 12:00)
    time_style = NamedStyle(name="time_style")
    time_style.number_format = 'HH:MM'
    time_style.font = Font(size=11, name='Segoe UI', color=TEXTO_OSCURO)
    time_style.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )
    
    # Añadir estilos al libro
    for style in [header_style, data_style, money_style, date_style, time_style, even_row_style, odd_row_style]:
        wb.add_named_style(style)
    
    # =============================================
    # CONSTRUCCIÓN DEL EXCEL
    # =============================================
    
    # Título principal
    ws.merge_cells('A1:I1')
    title_cell = ws['A1']
    title_cell.value = "HISTORIAL DE TRABAJOS"
    title_cell.font = Font(bold=True, size=14, color=AZUL_OSCURO, name='Segoe UI')
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    title_cell.fill = PatternFill(
        start_color=GRIS_CLARO,
        end_color=GRIS_CLARO,
        fill_type="solid"
    )
    
    # Subtítulo con información de filtros
    if funcionario or fecha_desde or fecha_hasta or estado:
        ws.merge_cells('A2:I2')
        subtitle = "Filtros aplicados: "
        filters = []
        if funcionario:
            filters.append(f"Funcionario: {funcionario}")
        if fecha_desde:
            filters.append(f"Desde: {fecha_desde}")
        if fecha_hasta:
            filters.append(f"Hasta: {fecha_hasta}")
        if estado:
            filters.append(f"Estado: {estado}")
        
        subtitle += " | ".join(filters)
        subtitle_cell = ws['A2']
        subtitle_cell.value = subtitle
        subtitle_cell.font = Font(size=10, italic=True, color=AZUL_MEDIO, name='Segoe UI')
        subtitle_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Encabezados comienzan en fila 3
        start_row = 3
    else:
        start_row = 2
    
    # Encabezados de columnas
    headers = [
        "Funcionario", "Sitio", "Cliente", 
        "Descripción", "Fecha", "H. Inicio", 
        "H. Salida", "Estado", "Monto (Gs)"
    ]
    ws.append(headers)
    
    # Aplicar estilo a los encabezados
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=start_row, column=col)
        cell.style = header_style
    
    # Filas de datos
    for t in trabajos:
        row = [
            str(t.tec_nombre),
            str(t.tec_sitios),
            t.tec_cliente,
            t.tec_descripcion,
            t.tec_fecha,
            t.tec_hinicio.strftime("%H:%M") if t.tec_hinicio else "",  # Formato 12:00
            t.tec_hfinal.strftime("%H:%M") if t.tec_hfinal else "",    # Formato 12:00
            str(t.tec_ee),  # Estado con estilo uniforme
            int(t.tec_tm.tm_monto) if t.tec_tm else 0,
        ]
        ws.append(row)
        
        current_row = ws.max_row
        row_style = even_row_style if current_row % 2 == 0 else odd_row_style
        
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=current_row, column=col)
            cell.style = data_style
            cell.fill = row_style.fill
            
            # Aplicar estilos especiales
            if col == 5:  # Fecha
                cell.style = date_style
            elif col in [6, 7]:  # Horas
                cell.style = time_style
            elif col == 9:  # Monto
                cell.style = money_style
                cell.value = int(cell.value) if cell.value else 0
    
    # =============================================
    # AJUSTES FINALES
    # =============================================
    
    # Ajustar ancho de columnas
    column_widths = {
        'A': 25,  # Funcionario
        'B': 20,  # Sitio
        'C': 25,  # Cliente
        'D': 40,  # Descripción
        'E': 12,  # Fecha
        'F': 10,  # H. Inicio
        'G': 10,  # H. Salida
        'H': 15,  # Estado
        'I': 15   # Monto
    }
    
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width
    
    # Congelar encabezados
    ws.freeze_panes = f"A{start_row + 1}"
    
    # Añadir filtros
    ws.auto_filter.ref = f"A{start_row}:I{ws.max_row}"
    
    # Añadir bordes decorativos
    for row in ws.iter_rows(min_row=start_row, max_row=ws.max_row, min_col=1, max_col=9):
        for cell in row:
            if cell.row == start_row:  # Encabezados
                cell.border = Border(
                    bottom=Side(border_style="medium", color=AZUL_OSCURO),
                    top=Side(border_style="medium", color=AZUL_OSCURO),
                    left=Side(border_style="thin", color=AZUL_MEDIO + "80"),
                    right=Side(border_style="thin", color=AZUL_MEDIO + "80")
                )
            elif cell.row == ws.max_row:  # Última fila
                cell.border = Border(
                    bottom=Side(border_style="medium", color=GRIS_MEDIO),
                    left=Side(border_style="thin", color=GRIS_MEDIO),
                    right=Side(border_style="thin", color=GRIS_MEDIO)
                )
    
    # Añadir línea decorativa azul al final
    ws.merge_cells(f'A{ws.max_row + 1}:I{ws.max_row + 1}')
    decor_cell = ws[f'A{ws.max_row}']
    decor_cell.fill = PatternFill(
        start_color=AZUL_CLARO,
        end_color=AZUL_CLARO,
        fill_type="solid"
    )
    ws.row_dimensions[ws.max_row].height = 3
    
    # Preparar respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="Historial_Trabajos_{datetime.now().strftime("%Y%m%d")}.xlsx"'
    wb.save(response)
    
    return response
