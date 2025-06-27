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
            tarea_dpto__dpto_nombre__in=["TTHH", "General"]
        )