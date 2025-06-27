from django import forms 
from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *
# añadir tarea
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['tarea_titulo', 'tarea_descripcion', 'tarea_te', 'tarea_td']
        labels = {
            'tarea_titulo': 'Título',
            'tarea_descripcion': 'Descripción',
            'tarea_te': 'Estado',
            'tarea_td': 'Día',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir el día "General"
        self.fields['tarea_td'].queryset = Tareadia.objects.exclude(td_dia="General")
         # Excluir estados que contienen la palabra "General" (puede estar en cualquier parte del texto)
        self.fields['tarea_te'].queryset = Tareaestado.objects.exclude(te_estado__icontains="General")

# eliminar tarea
class EliminarTareaForm(forms.Form):
    tarea_titulo = forms.ModelChoiceField(
        queryset=Tareas.objects.none(),  # Se define dinámicamente en __init__
        empty_label="Selecciona una tarea",
        label="Título de la tarea",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tarea_titulo'].queryset = Tareas.objects.filter(
            tarea_dpto__dpto_nombre="Informatica"
        ).exclude(
            tarea_td__td_dia__iexact="General"
        )

# AÑADIR A BACKUPS SEMANALES
class BackupForm(forms.ModelForm):
    class Meta:
        model = Backupsproceso
        fields = ["bp_bd", "bp_b", "bp_be"]

    def __init__(self, *args, **kwargs):
        super(BackupForm, self).__init__(*args, **kwargs)
        # Filtramos para mostrar solo los backups con estado activo
        self.fields['bp_b'].queryset = Backups.objects.filter(b_estado='activo')
        
# AÑADIR UN BACKUP A UN FUNCIONARIO CON EQUIPO
class BackupsProcesoForm(forms.ModelForm):
    class Meta:
        model = Backups
        fields = ["b_fce", "b_disco", "b_equipo", "b_nombre","b_estado"]
        
# AÑADIR UN FUNCIONARIO CON EQUIPO
class fceForm(forms.ModelForm):
    class Meta:
        model = Funcionarioconequipo
        fields = [
            "fce_equipo", "fce_fun", "fce_nombre_equipo", 
            "fce_nombre_sati", "fce_serie_sati", "fce_ip", 
            "fce_observaciones", "fce_ruta_imagen", "fce_estado"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar el queryset del campo fce_fun para que solo aparezcan los activos
        self.fields['fce_fun'].queryset = Funcionarios.objects.filter(fun_estado="activo") 

# AÑADIR RAK
class rakForm(forms.ModelForm):
    class Meta:
        model = InventarioinformaticaDeposito
        fields = ["iid_nombre"]
        
# AÑADIR ESTADO(inventario)
class StatusForm(forms.ModelForm):
    class Meta:
        model = InventarioinformaticaEstado
        fields = ["iie_nombre"]
        
# AÑADIR UN ITEM
class ItemForm(forms.ModelForm):
    class Meta:
        model = InventarioinformaticaCategoria
        fields = ["iic_nombre"]
        
# AÑADIR UN NUEVO ARTICULO
class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Inventarioinformatica
        fields = ["ii_iic","ii_iid","ii_cantidad","ii_iie","ii_descripcion"]
   
# añadir nuevo equipo     
class NewEquipo(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = ["eq_id","eq_tipe","eq_numdeserie","eq_dpto","eq_usuario","eq_contrasenna","eq_marca","eq_modelo","eq_marcamonitor","eq_pulgadamonitor","eq_placamadre","eq_grafica","eq_discoduro","eq_lectordisco","eq_audio","eq_sistemop"]
    def __init__(self, *args, **kwargs):
        super(NewEquipo, self).__init__(*args, **kwargs)
        # Filtrar las opciones del campo eq_tipe solo a "PC" y "Notebook"
        self.fields['eq_tipe'].queryset = Tipoequipo.objects.filter(tipe_nombre__in=["PC", "Notebook"])
        
# añadir nueva ups
class NewUps(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = ["eq_id", "eq_tipe", "eq_numdeserie", "eq_dpto", "eq_usuario", "eq_marca", "eq_modelo"]

    def __init__(self, *args, **kwargs):
        super(NewUps, self).__init__(*args, **kwargs)
        # Buscar el objeto Tipoequipo con nombre "UPS"
        ups_tipe = Tipoequipo.objects.filter(tipe_nombre="UPS").first()
        self.fields['eq_tipe'].initial = ups_tipe  # Valor por defecto
        self.fields['eq_tipe'].disabled = True     
        
# añadir nueva impresora
class NewImpresora(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = ["eq_id", "eq_tipe", "eq_numdeserie", "eq_dpto", "eq_usuario", "eq_marca", "eq_modelo"]

    def __init__(self, *args, **kwargs):
        super(NewImpresora, self).__init__(*args, **kwargs)
        impresora_tipe = Tipoequipo.objects.filter(tipe_nombre="Impresora").first()
        self.fields['eq_tipe'].initial = impresora_tipe  # Valor preseleccionado
        self.fields['eq_tipe'].disabled = True           # Deshabilitado para que no se pueda cambiar
        
# añadir otros a equipos
class NewOtros(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = ["eq_id","eq_tipe","eq_numdeserie","eq_dpto","eq_usuario","eq_marca","eq_modelo","eq_discoduro"]
    def __init__(self, *args, **kwargs):
        super(NewOtros, self).__init__(*args, **kwargs)
        # Filtrar las opciones del campo eq_tipe solo a "Router","DVR","Laser";"Scaner"
        self.fields['eq_tipe'].queryset = Tipoequipo.objects.filter(tipe_nombre__in=["Router", "DVR", "Laser", "Scaner"])    
        
# añadir cosas de servidor
class NewCosasServidor(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = ["eq_id","eq_tipe","eq_numdeserie","eq_dpto","eq_usuario","eq_marca","eq_modelo","eq_discoduro"]
    def __init__(self, *args, **kwargs):
        super(NewCosasServidor, self).__init__(*args, **kwargs)
        # Filtrar las opciones del campo eq_tipe solo a "PC" y "Notebook"
        self.fields['eq_tipe'].queryset = Tipoequipo.objects.filter(tipe_nombre__in=["Rack", "Switch"])

# añadir monitores
class NewMonitor(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = ["eq_id","eq_tipe","eq_numdeserie","eq_dpto","eq_usuario","eq_marcamonitor","eq_pulgadamonitor"]
    def __init__(self, *args, **kwargs):
        super(NewMonitor, self).__init__(*args, **kwargs)
        # Buscar el objeto Tipoequipo con nombre "Monitor"
        monitor_tipe = Tipoequipo.objects.filter(tipe_nombre="Monitor").first()
        self.fields['eq_tipe'].initial = monitor_tipe  # Valor por defecto
        self.fields['eq_tipe'].disabled = True         # Campo no editable
        
# añadir mantenimiento
class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimientocalendario
        fields = ["mc_fecha","mc_mt","mc_eq","mc_me"]

    def __init__(self, *args, **kwargs):
        super(MantenimientoForm, self).__init__(*args, **kwargs)
        # Buscar el objeto Mantenimientoestado con me_estado = "Pendiente⚠️"
        pendiente_estado = Mantenimientoestado.objects.filter(me_estado="Pendiente⚠️").first()
        self.fields['mc_me'].initial = pendiente_estado  # Asignar como valor por defecto
        # Opcional: deshabilitar el campo para que no se pueda cambiar
        self.fields['mc_me'].disabled = True
        
        # Añadir atributos personalizados
        self.fields['mc_fecha'].widget.attrs.update({
            'placeholder': 'DD/MM/AAAA'
        })
        
        