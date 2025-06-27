from django import forms 
from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *

# Entrada de Funcionarios
class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnicos
        fields = ["tec_sitios","tec_cliente","tec_descripcion","tec_fecha","tec_hinicio","tec_hfinal"]
        labels = {
            'tec_sitios': 'Sitio',
            'tec_cliente': 'Cliente',
            'tec_descripcion':  'Descripción',
            'tec_fecha':'Fecha',
            'tec_hinicio':'Hora de Inicio',
            'tec_hfinal':'Hora de Finalización',
        }
        widgets = {
            'tec_sitios': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Oficina Central'}),
            'tec_cliente': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre del cliente'}),
            'tec_descripcion': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Describe el trabajo...', 'rows': 3}),
            'tec_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-date'}),
            'tec_hinicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-time'}),
            'tec_hfinal': forms.TimeInput(attrs={'type': 'time', 'class': 'form-time'}),
        }

   

    def clean_tec_sitios(self):
        sitio = self.cleaned_data.get('tec_sitios')
        return sitio if sitio else "-"
